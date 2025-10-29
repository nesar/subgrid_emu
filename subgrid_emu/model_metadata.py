"""
Model metadata containing information about the training data grids.

This module stores the x-grids (independent variables) and parameter information
that was used to train each model. This is needed to properly load the models.
"""

import numpy as np

# Grid information for each statistic
# These are the actual grids used during training

TRAINING_GRIDS = {
    'GSMF': {
        'y_ind': np.logspace(9, 12, 39),  # stellar mass
        'n_params': 5,
        'exp_variance': 0.95
    },
    'BHMSM': {
        'y_ind': np.logspace(10, 12.5, 20),  # stellar mass
        'n_params': 5,
        'exp_variance': 0.95
    },
    'fGas': {
        'y_ind': np.logspace(13.5, 14.5, 40),  # halo mass
        'n_params': 5,
        'exp_variance': 0.95
    },
    'CGD': {
        'y_ind': 10**np.linspace(-2, 0.5, 21)[1:],  # radius (skip first)
        'n_params': 5,
        'exp_variance': 0.95
    },
    'Pk': {
        'y_ind': np.logspace(np.log10(0.04908738521234052), np.log10(12.566370614359172), 443),
        'n_params': 5,
        'exp_variance': 0.95
    },
    'CSFR': {
        'y_ind': np.linspace(0.1, 1.0, 655),  # scale factor
        'n_params': 5,
        'exp_variance': 0.95
    },
    'CGD_2p': {
        'y_ind': 10**np.linspace(-2, 0.5, 21)[1:],  # radius (skip first)
        'n_params': 2,
        'exp_variance': 0.99
    },
    'fGas_2p': {
        'y_ind': np.logspace(13.5, 14.5, 40),  # halo mass
        'n_params': 2,
        'exp_variance': 0.99
    },
}


def get_training_grid(stat_name):
    """
    Get the training grid information for a statistic.
    
    Parameters
    ----------
    stat_name : str
        Name of the summary statistic
        
    Returns
    -------
    dict
        Dictionary with 'y_ind', 'n_params', and 'exp_variance'
    """
    if stat_name not in TRAINING_GRIDS:
        raise ValueError(f"Unknown statistic: {stat_name}")
    
    return TRAINING_GRIDS[stat_name]
