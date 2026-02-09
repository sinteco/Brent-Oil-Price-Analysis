import pymc as pm
import numpy as np
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt

import pytensor.tensor as pt

def run_multi_change_point_model(df, k=2, n_samples=1000, tune=1000):
    """
    Fits a Bayesian Change Point model to the Brent oil prices with k change points.
    """
    data = np.log(df['Price'].values)
    n_data = len(data)
    idx = np.arange(n_data)
    
    with pm.Model() as model:
        # Priors for the change points (tau_1, tau_2, ..., tau_k)
        tau = pm.Uniform("tau", lower=0, upper=n_data, shape=k)
        tau_sorted = pm.Deterministic("tau_sorted", pt.sort(tau))
        
        # Priors for the means in each segment
        mu = pm.Normal("mu", mu=data.mean(), sigma=data.std(), shape=k+1)
        
        # Priors for the standard deviation
        sigma = pm.HalfNormal("sigma", sigma=data.std())
        
        # Assignment of the mean based on the change points
        # Use pytensor.switch for better performance and consistency
        mu_ = mu[0]
        for i in range(k):
            mu_ = pm.math.switch(idx > tau_sorted[i], mu[i+1], mu_)
        
        # Likelihood
        observation = pm.Normal("obs", mu=mu_, sigma=sigma, observed=data)
        
        # Sampling
        trace = pm.sample(n_samples, tune=tune, target_accept=0.9, cores=1, random_seed=42)
        
    return trace

if __name__ == "__main__":
    # Example usage for the last decade
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    # Filter for a specific period to make it faster for demonstration
    # Let's take 2018-2022 to capture 2020 crash and 2022 surge
    df_recent = df[df.index >= '2018-01-01']
    
    print(f"Running model on {len(df_recent)} data points with k=2 change points...")
    trace = run_multi_change_point_model(df_recent, k=2)
    
    # Save results summary
    summary = az.summary(trace, var_names=["tau_sorted", "mu", "sigma"])
    print(summary)
    
    # Plot posterior distributions
    az.plot_trace(trace, var_names=["tau_sorted", "mu", "sigma"])
    plt.tight_layout()
    plt.savefig("notebooks/model_trace_multi.png")
    print("Model trace saved to notebooks/model_trace_multi.png")
    
    # Map tau indices back to dates
    tau_samples = trace.posterior["tau_sorted"].values.reshape(-1, 2)
    tau_means = tau_samples.mean(axis=0)
    
    dates = df_recent.index
    change_point_dates = [dates[int(t)] for t in tau_means]
    print(f"Detected change point dates: {change_point_dates}")
