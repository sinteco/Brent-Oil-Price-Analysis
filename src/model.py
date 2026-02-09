import pymc as pm
import numpy as np
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt
import pytensor.tensor as pt

def run_advanced_change_point_model(df, k=3, n_samples=1000, tune=500):
    """
    Fits an optimized Bayesian Change Point model with k=3.
    """
    data = np.log(df['Price'].values)
    n_data = len(data)
    idx = np.arange(n_data)
    
    with pm.Model() as model:
        tau = pm.Uniform("tau", lower=0, upper=n_data, shape=k)
        tau_sorted = pm.Deterministic("tau_sorted", pt.sort(tau))
        mu = pm.Normal("mu", mu=data.mean(), sigma=data.std(), shape=k+1)
        sigma = pm.HalfNormal("sigma", sigma=data.std(), shape=k+1)
        
        mu_ = mu[0]
        sigma_ = sigma[0]
        for i in range(k):
            mu_ = pm.math.switch(idx > tau_sorted[i], mu[i+1], mu_)
            sigma_ = pm.math.switch(idx > tau_sorted[i], sigma[i+1], sigma_)
        
        observation = pm.Normal("obs", mu=mu_, sigma=sigma_, observed=data)
        trace = pm.sample(n_samples, tune=tune, target_accept=0.9, cores=1, random_seed=42)
        
    return trace

if __name__ == "__main__":
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    df_recent = df[(df.index >= '2020-01-01') & (df.index <= '2022-12-31')]
    
    k_val = 2
    print(f"Running optimized model (2020-2022) with k={k_val}...")
    trace = run_advanced_change_point_model(df_recent, k=k_val)
    
    # Save results
    summary = az.summary(trace, var_names=["tau_sorted", "mu", "sigma"])
    print(summary)
    summary.to_csv("data/processed/model_summary_k5.csv")
    
    # Plotting
    az.plot_trace(trace, var_names=["tau_sorted", "mu", "sigma"])
    plt.tight_layout()
    plt.savefig("notebooks/advanced_model_trace.png")
    
    # Map tau to dates and save
    tau_means = trace.posterior["tau_sorted"].values.reshape(-1, k_val).mean(axis=0)
    dates = df_recent.index
    change_point_dates = [dates[int(t)] for t in tau_means]
    
    cp_df = pd.DataFrame({'Change_Point_Index': tau_means, 'Date': change_point_dates})
    cp_df.to_csv("data/processed/detected_change_points.csv", index=False)
    print(f"Detected dates saved: {change_point_dates}")
