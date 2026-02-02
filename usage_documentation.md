# Subgrid Emulator Usage Documentation

## Overview

The `subgrid_emu` package provides emulators for various cosmological summary statistics. There are two types of models:
- **5-parameter models**: GSMF, CGD, fGas, BHMSM, CSFR, Pk
- **2-parameter models**: CGD_2p, fGas_2p, Pk_2p

## Basic Usage

### Loading and Using 5-Parameter Models

```python
from subgrid_emu import load_emulator

# Load a 5-parameter emulator
emu = load_emulator('GSMF')

# Make predictions with 5 parameters: [kappa, e_gw, seed_mass, vkin, eps]
params = [3.0, 0.5, 0.8, 0.65, 0.1]
mean, std = emu.predict(params)
```

### Loading and Using 2-Parameter Models

```python
# Load a 2-parameter emulator
emu = load_emulator('CGD_2p')

# Make predictions with 2 parameters: [vkin, eps]
params = [0.65, 0.1]
mean, std = emu.predict(params)
```

## Parameter Scaling

Parameters should be provided in scaled units:
- `vkin`: Scaled by 1e4 (so 0.65 represents 6500 km/s)
- `eps`: Scaled by 1e1 (so 0.1 represents 1.0)
- `seed_mass`: Scaled by 1e6 (for 5-param models)

## Available Statistics

### 5-Parameter Models
- **GSMF**: Galaxy Stellar Mass Function
- **CGD**: Cluster Gas Density
- **fGas**: Gas Fraction
- **BHMSM**: Black Hole Mass - Stellar Mass
- **CSFR**: Cosmic Star Formation Rate
- **Pk**: Power Spectrum

### 2-Parameter Models
- **CGD_2p**: Cluster Gas Density (2-param version)
- **fGas_2p**: Gas Fraction (2-param version)
- **Pk_2p**: Power Spectrum (2-param version)

## Output Transformations

The emulator automatically applies appropriate transformations:
- **GSMF**: Output is transformed to log10 space
- **BHMSM**: Output is transformed from log10 to linear space (10^x)
- Other statistics are returned as-is

## Example from Notebooks

From the analysis of the Jupyter notebooks, here's how the models are typically used in practice:

### MCMC Analysis Example (from gp_HACC2p_mcmc_CGD.ipynb)

```python
# Load model
sepia_model_CGD = load_model('model/CGDDec26_2p_multivariate_model_z_index0',
                              p_all=params32,
                              y_vals=y_vals_cgd,
                              y_ind=y_ind_cgd)

# Make predictions
model_grid, model_var_grid = emulate(sepia_model_CGD, params_calib)

# Plot results
plt.plot(y_ind_cgd, model_grid, 'k', label='256 Mpc box: CGD')
plt.plot(y_ind_cgd, model_var_grid[:, :, 0], 'k-.')  # Lower uncertainty
plt.plot(y_ind_cgd, model_var_grid[:, :, 1], 'k-.')  # Upper uncertainty
```

### Parameter Ranges

Based on the notebooks, typical parameter ranges are:
- **vkin**: 0.25 to 1.0 (scaled, representing 2500-10000 km/s)
- **eps**: 0.02 to 0.5 (scaled, representing 0.2-5.0)

## Technical Notes

### 2-Parameter Model Issues

The 2-parameter models were trained with observational data included in the SEPIA framework, which creates a different internal structure. The models have:
- betaU shape of (3, n_pc) instead of (2, n_pc)
- This indicates they were trained with 2 simulation parameters + 1 observational parameter

### Current Limitations

Due to the way 2-parameter models were trained, there are currently issues with loading them directly through the standard interface. A workaround is being developed to handle the observational data structure properly.

## Recommended Usage Pattern

For robust usage, especially with 2-parameter models:

```python
import numpy as np
from subgrid_emu import load_emulator

# For 5-parameter models
emu_5p = load_emulator('GSMF')
params_5p = np.array([3.0, 0.5, 0.8, 0.65, 0.1])
mean_5p, std_5p = emu_5p.predict(params_5p)

# For 2-parameter models (once fixed)
emu_2p = load_emulator('CGD_2p')
params_2p = np.array([0.65, 0.1])
mean_2p, std_2p = emu_2p.predict(params_2p)

# Multiple predictions at once
params_multiple = np.array([
    [0.65, 0.1],
    [0.50, 0.2],
    [0.75, 0.05]
])
means, stds = emu_2p.predict(params_multiple)
```

## Integration with MCMC

The emulators are designed to work with MCMC sampling frameworks. The notebooks show examples of using the emulators with:
- Prior distributions on parameters
- Log-likelihood calculations comparing to observational data
- Posterior sampling using emcee or similar packages
