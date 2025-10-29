"""
Subgrid Physics Emulator Package

A Python package for emulating cosmological hydrodynamical simulation outputs
using Gaussian Process emulators trained on the HACC simulation suite.

This package provides fast predictions for various summary statistics as a
function of subgrid physics parameters, without needing to run full simulations.

Examples
--------
Basic usage:

>>> from subgrid_emu import load_emulator
>>> 
>>> # Load an emulator for Galaxy Stellar Mass Function
>>> emu = load_emulator('GSMF')
>>> 
>>> # Define parameters: [kappa_w, e_w, M_seed/1e6, v_kin/1e4, eps/1e1]
>>> params = [3.0, 0.5, 0.8, 0.65, 0.1]
>>> 
>>> # Make prediction
>>> mean, quantiles = emu.predict(params)
>>> 
>>> # mean contains the predicted GSMF
>>> # quantiles contains [5%, 95%] uncertainty bounds

Available summary statistics:
- GSMF: Galaxy Stellar Mass Function
- BHMSM: Black Hole Mass - Stellar Mass relation
- fGas: Cluster Gas Fraction
- CGD: Cluster Gas Density profile
- CGED: Cluster Gas Electron Density profile
- Pk: Matter Power Spectrum ratio (hydro/gravity-only)
- CSFR: Cosmic Star Formation Rate
- CGD_2p: Cluster Gas Density (2-parameter model)
- CGD_CC_2p: Cluster Gas Density Cool Core (2-parameter model)
- fGas_2p: Cluster Gas Fraction (2-parameter model)
"""

__version__ = '0.1.0'
__author__ = 'Nesar Ramachandra'

from .emulator import (
    SubgridEmulator,
    load_emulator,
    list_available_statistics,
    PARAM_NAMES,
    AVAILABLE_STATS_5P,
    AVAILABLE_STATS_2P,
    SEED_MASS_SCALE,
    VKIN_SCALE,
    EPS_SCALE
)

from .data_utils import (
    get_x_grid,
    get_plot_info,
    get_valid_range,
    get_parameter_info
)

__all__ = [
    # Main classes and functions
    'SubgridEmulator',
    'load_emulator',
    'list_available_statistics',
    
    # Constants
    'PARAM_NAMES',
    'AVAILABLE_STATS_5P',
    'AVAILABLE_STATS_2P',
    'SEED_MASS_SCALE',
    'VKIN_SCALE',
    'EPS_SCALE',
    
    # Data utilities
    'get_x_grid',
    'get_plot_info',
    'get_valid_range',
    'get_parameter_info',
]
