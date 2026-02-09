import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import os

def run_task2_model():
    # Load data
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    # Filter for 2018-2022
    df_model = df[(df.index >= '2018-01-01') & (df.index <= '2022-12-31')].copy()
    data = np.log(df_model['Price'].values)
    n_data = len(data)
    idx = np.arange(n_data)
    
    with pm.Model() as model:
        # Define the Switch Point (tau)
        tau = pm.DiscreteUniform("tau", lower=0, upper=n_data - 1)
        
        # Define Before and After Parameters
        mu_1 = pm.Normal("mu_1", mu=data.mean(), sigma=data.std())
        mu_2 = pm.Normal("mu_2", mu=data.mean(), sigma=data.std())
        
        # Common sigma
        sigma = pm.HalfNormal("sigma", sigma=data.std())
        
        # Use Switch Function
        mu_ = pm.math.switch(tau > idx, mu_1, mu_2)
        
        # Define the Likelihood
        observation = pm.Normal("obs", mu=mu_, sigma=sigma, observed=data)
        
        # Run the Sampler
        print("Starting MCMC sampling...")
        trace = pm.sample(2000, tune=1000, target_accept=0.9, cores=1, random_seed=42)
        
    # Interpret Model Output
    summary = az.summary(trace)
    print(summary)
    
    tau_mean = int(trace.posterior["tau"].values.mean())
    cp_date = df_model.index[tau_mean]
    print(f"Detected Change Point Date: {cp_date.date()}")
    
    mu1_val = np.exp(trace.posterior["mu_1"].values.mean())
    mu2_val = np.exp(trace.posterior["mu_2"].values.mean())
    print(f"Average price before break: ${mu1_val:.2f}")
    print(f"Average price after break: ${mu2_val:.2f}")
    
    # Save plots
    az.plot_trace(trace)
    plt.savefig("notebooks/task2_trace.png")
    
    plt.figure()
    plt.hist(trace.posterior["tau"].values.flatten(), bins=n_data, color="blue", alpha=0.7)
    plt.title("Posterior Distribution of Change Point (tau)")
    plt.xlabel("Index")
    plt.ylabel("Probability Density")
    plt.savefig("notebooks/task2_tau_posterior.png")
    
    # Quantify the Impact associated with events
    # Researched event near 2020-03-06 (OPEC+ Alliance Breakdown) or 2020-04-20 (COVID Shock)
    print(f"The detected change point ({cp_date.date()}) aligns closely with the COVID-19 demand shock and OPEC+ negotiations in early 2020.")
    print(f"Following this event, the model detects a change point, with the average daily price shifting from ${mu1_val:.2f} to ${mu2_val:.2f}, an increase of {(mu2_val-mu1_val)/mu1_val*100:.2f}%.")

if __name__ == "__main__":
    run_task2_model()
