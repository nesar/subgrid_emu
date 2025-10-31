# Emulator-suite for Cosmological summary statistics from hydrodynamical Cosmological simulation.  

A Python package for fast emulation of cosmological hydrodynamical simulation outputs using Gaussian Process emulators trained on the CRK-HACC simulation suite.

## Overview

This package provides trained surrogates that predict various cosmological summary statistics as a function of subgrid physics parameters. The emulators are based on Gaussian Processes and trained on a suite of 64 (5 subgrid parameters, smaller boxes) + 16 (2 subgrid parameters, larger boxes) simulations of with varying subgrid physics parameters.

## Installation

Clone the repository:

```bash
git clone https://github.com/nesar/subgrid_emu.git
cd subgrid_emu
pip install -e .
```

## Quick Start

```python
from subgrid_emu import load_emulator, get_x_grid

# Load an emulator for Galaxy Stellar Mass Function
emu = load_emulator('GSMF')

# Define subgrid physics parameters
# [kappa_w, e_w, M_seed, v_kin, epsilon_kin] (in scaled units)
params = [3.0, 0.5, 0.8, 0.65, 0.1]

# Make prediction
mean, quantiles = emu.predict(params)

# Get the x-axis values (stellar masses in this case)
x_grid, x_label = get_x_grid('GSMF')

# Plot the result
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 6))
plt.plot(x_grid, mean, label='Prediction')
plt.fill_between(x_grid, quantiles[:, 0], quantiles[:, 1], 
                 alpha=0.3, label='90% CI')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(x_label)
plt.ylabel('GSMF')
plt.legend()
plt.show()
```

## Available Summary Statistics

### 5-Parameter Models (smaller simulation box)

| Stat Name | LaTeX | Description |
|-----------|-------|-------------|
| GSMF | $\mathrm{d}n / \mathrm{d}\log_{10} M_{\mathrm{stars}} \left[1 / (h^{-1}\mathrm{Mpc})^3 \right]$ | Galaxy stellar mass function |
| CGD | $\rho_{\mathrm{gas}} / \rho_{\mathrm{crit}}$ | Cluster gas density |
| fGas | $M_{\mathrm{gas}} / M_{\mathrm{500c}} \quad [<R_{\mathrm{500c}}]$ | Cluster gas fraction |
| BHMSM | $M_{\mathrm{BH}} [\mathrm{M}_{\odot}$] | Black hole mass-stellar mass |
| CSFR | $\mathrm{CSFR}   [\mathrm{M}_{\odot}   \mathrm{yr}^{-1}   (h^{-1}\mathrm{Mpc})^{-3}]$ | Cosmic star formation rate |
| Pk | $P_{\mathrm{sub}}(k) / P_{\mathrm{grav}}(k)$ | Total power spectra ratio |

### 2-Parameter Models (larger simulation box)

| Stat Name | LaTeX | Description |
|-----------|-------|-------------|
| CGD_2p | $\rho_{\mathrm{gas}}  /  \rho_{\mathrm{crit}}$ | Cluster gas density (higher resolution) |
| fGas_2p | $M_{\mathrm{gas}} / M_{\mathrm{500c}} \quad [<R_{\mathrm{500c}}]$ | Cluster gas fraction (higher resolution) |

## Input Parameters

| # | Parameter | LaTeX | Range | Description |
|---|-----------|-------|-------|-------------|
| 1 | kappa_w | $\kappa_\text{w}$ | (2.0, 4.0) | Wind efficiency parameter |
| 2 | e_w | $e_\text{w}$ | (0.2, 1.0) | Wind energy fraction |
| 3 | M_seed | $M_\text{seed}/10^{6}$ | (0.6, 1.2) | Black hole seed mass (in 10^6 M_☉) |
| 4 | v_kin | $v_\text{kin}/10^{4}$ | (0.1, 1.2) | Kinetic wind velocity (in 10^4 km/s) |
| 5 | epsilon_kin | $\epsilon_\text{kin}/10^{1}$ | (0.02, 1.2) | Kinetic feedback efficiency (in 10^1) |

**Note**: Parameters should be provided in the scaled units shown above.

## Examples

### List Available Statistics

```python
from subgrid_emu import list_available_statistics

stats = list_available_statistics()
print("5-parameter models:", stats['5-parameter'])
print("2-parameter models:", stats['2-parameter'])
```

### Get Parameter Information

```python
from subgrid_emu import get_parameter_info

param_info = get_parameter_info()
print("Parameter names:", param_info['names'])
print("Parameter ranges:", param_info['ranges'])
print("Descriptions:", param_info['descriptions'])
```

### Multiple Predictions

```python
import numpy as np
from subgrid_emu import load_emulator

# Load emulator
emu = load_emulator('CSFR')

# Create a grid of parameters
n_samples = 10
params_grid = np.random.uniform(
    low=[2.0, 0.2, 0.6, 0.1, 0.02],
    high=[4.0, 1.0, 1.2, 1.2, 1.2],
    size=(n_samples, 5)
)

# Make predictions for all parameter sets
for i, params in enumerate(params_grid):
    mean, quantiles = emu.predict(params)
    print(f"Prediction {i+1}: mean shape = {mean.shape}")
```

### Using 2-Parameter Models

```python
from subgrid_emu import load_emulator

# Load 2-parameter model
emu = load_emulator('CGD_2p')

# Only need last 2 parameters: [v_kin, epsilon_kin] (in scaled units)
params_2p = [0.65, 0.1]

mean, quantiles = emu.predict(params_2p)
```




## API Reference

### Main Functions

#### `load_emulator(stat_name, z_index=0, exp_variance=None)`
Load an emulator for a specific summary statistic.

**Parameters:**
- `stat_name` (str): Name of the summary statistic
- `z_index` (int): Redshift index (default: 0 for z=0)
- `exp_variance` (float): Explained variance for PCA (default: 0.95 for 5-param, 0.99 for 2-param)

**Returns:**
- `SubgridEmulator`: Loaded emulator object

#### `SubgridEmulator.predict(params, num_samples=100)`
Make predictions for given parameters.

**Parameters:**
- `params` (array-like): Input parameters (5 or 2 values depending on model)
- `num_samples` (int): Number of posterior samples for uncertainty quantification

**Returns:**
- `mean` (np.array): Mean prediction
- `quantiles` (np.array): [5%, 95%] prediction quantiles

### Utility Functions

#### `get_x_grid(stat_name)`
Get the independent variable grid for a summary statistic.

**Returns:**
- `x_grid` (np.array): Grid values
- `x_label` (str): Label for the x-axis

#### `get_plot_info(stat_name)`
Get plotting information (title, labels, scales).

**Returns:**
- `dict`: Dictionary with 'title', 'xlabel', 'ylabel', 'xscale', 'yscale'

#### `get_valid_range(stat_name)`
Get the valid/recommended prediction range.

**Returns:**
- `tuple`: (min_value, max_value)

#### `get_parameter_info()`
Get detailed information about input parameters.

**Returns:**
- `dict`: Parameter names, ranges, descriptions, and scaling factors
