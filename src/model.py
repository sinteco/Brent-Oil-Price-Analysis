"""
Bayesian Change Point Detection Model
======================================
Workflow Step 6: Structural Break Modeling

This script implements a Bayesian Multi-Change Point Model using PyMC to detect
regime shifts in Brent oil prices.

Model Design:
    The time series is partitioned into (k+1) regimes by k change points (τ).
    Each regime has its own mean (μ) and standard deviation (σ). The model infers
    the posterior distributions of τ, μ, and σ via MCMC sampling.

    Formally:
        τ_1, ..., τ_k  ~ Uniform(0, N)            [sorted]
        μ_0, ..., μ_k   ~ Normal(mean(y), 10×std(y))  [weakly informative]
        σ_0, ..., σ_k   ~ HalfNormal(2×std(y))        [positive-constrained]
        y[t]            ~ Normal(μ_j, σ_j) where j = regime at time t

Assumptions:
    - Structural breaks are discrete, instantaneous transitions (not gradual).
    - Log-transformed prices are used to stabilize variance and reduce
      heteroscedasticity before modeling.
    - The number of change points (k) is pre-specified by the analyst. This is a
      model hyperparameter, not learned. Different k values yield different
      segmentations; k should be chosen via domain knowledge or model comparison.
    - Priors are deliberately weakly informative — the data dominates inference.

Limitations:
    - Discrete τ with Metropolis sampling can be slow to converge. Consider
      Sequential Monte Carlo (SMC) for multi-modal posteriors.
    - The model does not incorporate exogenous variables (GDP, USD index,
      OPEC quotas), so detected breaks are associative, not causal.
    - Results depend on the date window selected for analysis.
"""

import pymc as pm
import numpy as np
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt
import pytensor.tensor as pt
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def validate_model_input(df, k):
    """Validate modeling inputs before running MCMC."""
    if 'Price' not in df.columns:
        raise ValueError("DataFrame must contain a 'Price' column.")

    if df['Price'].isna().any():
        raise ValueError(f"Input contains {df['Price'].isna().sum()} NaN values. Clean data first.")

    if (df['Price'] <= 0).any():
        raise ValueError("Non-positive prices detected. Log transform will fail.")

    if len(df) < 50:
        raise ValueError(f"Too few observations ({len(df)}). Need at least 50 for reliable inference.")

    if not isinstance(k, int) or k < 1:
        raise ValueError(f"k must be a positive integer, got {k}.")

    if k >= len(df) // 20:
        logger.warning(f"k={k} is high relative to data size ({len(df)}). Regimes may have too few points.")

    logger.info(f"Model input validated: {len(df)} observations, k={k} change points.")


def validate_convergence(trace, var_names):
    """Check MCMC convergence diagnostics and log warnings."""
    try:
        summary = az.summary(trace, var_names=var_names)
        logger.info("=== Convergence Diagnostics ===")

        # Check R-hat
        if 'r_hat' in summary.columns:
            max_rhat = summary['r_hat'].max()
            if max_rhat > 1.05:
                logger.warning(f"R-hat = {max_rhat:.3f} (>1.05). Chains may not have converged. "
                               "Consider increasing tune/draws or using SMC.")
            else:
                logger.info(f"R-hat max = {max_rhat:.3f} (OK).")

        # Check ESS
        if 'ess_bulk' in summary.columns:
            min_ess = summary['ess_bulk'].min()
            if min_ess < 400:
                logger.warning(f"Min ESS = {min_ess:.0f} (<400). Posterior estimates may be unreliable.")
            else:
                logger.info(f"ESS min = {min_ess:.0f} (OK).")

        return summary
    except Exception as e:
        logger.error(f"Convergence check failed: {e}")
        return None


def run_change_point_model(df, k=3, n_samples=1000, tune=500):
    """
    Fit a Bayesian Multi-Change Point model.

    Args:
        df (pd.DataFrame): Cleaned price data with a 'Price' column and DatetimeIndex.
        k (int): Number of change points to detect (default: 3).
        n_samples (int): Number of posterior samples per chain (default: 1000).
        tune (int): Number of tuning steps per chain (default: 500).

    Returns:
        az.InferenceData: ArviZ trace object containing posterior samples.

    Raises:
        ValueError: If input data fails validation.
        RuntimeError: If MCMC sampling encounters errors.
    """
    validate_model_input(df, k)

    data = np.log(df['Price'].values)
    n_data = len(data)
    idx = np.arange(n_data)

    logger.info(f"Building PyMC model: k={k}, N={n_data}, samples={n_samples}, tune={tune}...")

    try:
        with pm.Model() as model:
            # --- Priors ---
            tau = pm.Uniform("tau", lower=0, upper=n_data, shape=k)
            tau_sorted = pm.Deterministic("tau_sorted", pt.sort(tau))
            mu = pm.Normal("mu", mu=data.mean(), sigma=data.std() * 10, shape=k + 1)
            sigma = pm.HalfNormal("sigma", sigma=data.std() * 2, shape=k + 1)

            # --- Regime assignment via switch ---
            mu_ = mu[0]
            sigma_ = sigma[0]
            for i in range(k):
                mu_ = pm.math.switch(idx > tau_sorted[i], mu[i + 1], mu_)
                sigma_ = pm.math.switch(idx > tau_sorted[i], sigma[i + 1], sigma_)

            # --- Likelihood ---
            observation = pm.Normal("obs", mu=mu_, sigma=sigma_, observed=data)

            # --- Sampling ---
            trace = pm.sample(n_samples, tune=tune, target_accept=0.9,
                              cores=1, random_seed=42)

        logger.info("MCMC sampling complete.")
        return trace

    except Exception as e:
        raise RuntimeError(f"MCMC sampling failed: {e}")


if __name__ == "__main__":
    data_path = "data/processed/BrentOilPrices_cleaned.csv"

    if not os.path.exists(data_path):
        logger.critical(f"Data file not found: {data_path}")
        sys.exit(1)

    try:
        df = pd.read_csv(data_path, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
    except Exception as e:
        logger.critical(f"Failed to load data: {e}")
        sys.exit(1)

    # Focus window
    df_recent = df[(df.index >= '2020-01-01') & (df.index <= '2022-12-31')]
    k_val = 2

    logger.info(f"Running model on {len(df_recent)} observations (2020-2022), k={k_val}...")

    try:
        trace = run_change_point_model(df_recent, k=k_val)

        # Convergence diagnostics
        summary = validate_convergence(trace, var_names=["tau_sorted", "mu", "sigma"])
        if summary is not None:
            os.makedirs("data/processed", exist_ok=True)
            summary.to_csv("data/processed/model_summary_k5.csv")
            print("\n" + summary.to_string())

        # Trace plot
        os.makedirs("notebooks", exist_ok=True)
        az.plot_trace(trace, var_names=["tau_sorted", "mu", "sigma"])
        plt.tight_layout()
        plt.savefig("notebooks/advanced_model_trace.png", dpi=150)
        plt.close()
        logger.info("Trace plot saved.")

        # Map τ to dates
        tau_means = trace.posterior["tau_sorted"].values.reshape(-1, k_val).mean(axis=0)
        dates = df_recent.index
        change_point_dates = []
        for t in tau_means:
            idx_int = int(np.clip(t, 0, len(dates) - 1))
            change_point_dates.append(dates[idx_int])

        cp_df = pd.DataFrame({'Change_Point_Index': tau_means, 'Date': change_point_dates})
        cp_df.to_csv("data/processed/detected_change_points.csv", index=False)
        logger.info(f"Change points saved: {change_point_dates}")

    except (ValueError, RuntimeError) as e:
        logger.critical(f"Model execution failed: {e}")
        sys.exit(1)
