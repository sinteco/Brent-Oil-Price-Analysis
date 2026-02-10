# Analysis Workflow, Assumptions & Limitations

## Data Analysis Workflow

The project follows a six-step sequential pipeline:

| Step | Script | Description |
|------|--------|-------------|
| 1. Data Acquisition | (Manual/FRED download) | Download daily Brent spot prices from FRED (1987–2026). |
| 2. Preprocessing | `src/data_preprocessing.py` | Parse dates, coerce prices to numeric, handle missing values via forward-fill/backward-fill, validate output integrity. |
| 3. EDA | `src/analyze_properties.py` | Compute trend (252-day rolling mean), test stationarity (ADF), measure volatility clustering (21-day annualized rolling std). |
| 4. Event Research | `data/external/major_events.csv` | Compile 15+ dated geopolitical/economic events from published sources. These are validation markers, **not** model inputs. |
| 5. Visualization | `src/generate_visuals.py` | Generate annotated time series plots with event overlay. |
| 6. Bayesian Modeling | `src/model.py` | Deploy PyMC Multi-Change Point model, assess convergence, extract change point dates. |

## Key Assumptions

1. **Data Source**: FRED is the authoritative source for Brent Crude spot prices.
2. **Missing Data**: Forward-fill followed by backward-fill is appropriate because oil markets do not trade on weekends/holidays, and prices persist until the next trading day.
3. **Stationarity Threshold**: An ADF p-value > 0.05 is interpreted as evidence of non-stationarity.
4. **Break Singularity**: The model assumes structural breaks occur instantaneously at a single point in time.
5. **Log Transform**: Prices are log-transformed before modeling to reduce heteroscedasticity.
6. **Prior Specification**: Weakly informative priors are used to let the data dominate inference.
7. **Correlation ≠ Causation**: Temporal proximity of a detected break to a known event does not prove the event caused the price shift.

## Known Limitations

1. **Univariate Analysis**: The model uses price alone. Exogenous variables (USD index, OPEC production, GDP) are not incorporated.
2. **Fixed k**: The number of change points is pre-specified, not learned. Different k values may yield different results.
3. **MCMC Convergence**: Discrete τ parameters use Metropolis sampling, which can be slow to converge and may exhibit multi-modality.
4. **No Inflation Adjustment**: Prices are nominal; real value comparisons across decades require deflation.
5. **Gradual Transitions**: Multi-year trends (e.g., renewable energy adoption) cannot be captured as point breaks.

## Expected Model Outputs

- **Posterior distribution of τ**: Probability distribution over candidate break dates.
- **Regime means (μ)**: Average price level within each detected regime.
- **Regime volatilities (σ)**: Standard deviation within each regime.
- **Convergence diagnostics**: R-hat (< 1.05) and ESS (> 400) for all parameters.
