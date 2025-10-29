"""
Data utilities for the subgrid emulator package.

This module provides information about the independent variables (x-grids)
for each summary statistic, as well as plotting utilities.
"""

import numpy as np
import os


def get_x_grid(stat_name, z_index=0):
    """
    Get the independent variable grid for a given summary statistic.
    
    This returns the actual x-grid used by the emulator (from training data).
    
    Parameters
    ----------
    stat_name : str
        Name of the summary statistic
    z_index : int, optional
        Redshift index (default: 0)
        
    Returns
    -------
    np.array
        Independent variable values
    str
        Description of the independent variable
        
    Examples
    --------
    >>> x_grid, x_label = get_x_grid('GSMF')
    >>> print(x_label)
    'Stellar mass [M_sun]'
    """
    
    # Load the actual y_ind from training data
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    base_name = f"{stat_name}_z_index{z_index}"
    y_ind_path = os.path.join(data_dir, f"{base_name}_y_ind.npy")
    
    if os.path.exists(y_ind_path):
        x_grid = np.load(y_ind_path)
    else:
        raise FileNotFoundError(
            f"Training data not found for {stat_name}. "
            f"Expected file: {y_ind_path}"
        )
    
    # Get the label based on statistic type
    if stat_name == 'GSMF':
        x_label = r'Stellar mass [$M_\odot$]'
        
    elif stat_name == 'BHMSM':
        x_label = r'Stellar mass [$M_\odot$]'
        
    elif stat_name in ['fGas', 'fGas_2p']:
        x_label = r'Halo mass $M_{500c}$ [$M_\odot$]'
        
    elif stat_name in ['CGD', 'CGD_2p']:
        x_label = r'Radius $r/R_{500c}$'
        
    elif stat_name == 'Pk':
        x_label = r'Wavenumber $k$ [$h$/Mpc]'
        
    elif stat_name == 'CSFR':
        x_label = r'Scale factor $a$'
        
    else:
        raise ValueError(
            f"Unknown statistic: {stat_name}\n"
            f"Available: GSMF, BHMSM, fGas, CGD, Pk, CSFR, "
            f"CGD_2p, fGas_2p"
        )
    
    return x_grid, x_label


def get_plot_info(stat_name):
    """
    Get plotting information for a summary statistic.
    
    Parameters
    ----------
    stat_name : str
        Name of the summary statistic
        
    Returns
    -------
    dict
        Dictionary with keys: 'title', 'xlabel', 'ylabel', 'xscale', 'yscale'
        
    Examples
    --------
    >>> info = get_plot_info('GSMF')
    >>> print(info['title'])
    'Galaxy stellar mass function'
    """
    
    if stat_name == 'GSMF':
        return {
            'title': 'Galaxy stellar mass function',
            'xlabel': r"$\log_{10} \left[ M_{\mathrm{stars}} / \mathrm{M}_{\odot}  \right]$",
            'ylabel': r"$\mathrm{d}n \, / \, \mathrm{d}\log_{10} M_{\mathrm{stars}}  \left[1 / (h^{-1}\mathrm{Mpc})^3  \right]$",
            'xscale': 'log',
            'yscale': 'log'
        }
        
    elif stat_name == 'BHMSM':
        return {
            'title': 'Black hole mass-stellar mass',
            'xlabel': r"$M_{\ast}$ [$\mathrm{M}_{\odot}$]",
            'ylabel': r"$M_{\mathrm{BH}}$ [$\mathrm{M}_{\odot}$]",
            'xscale': 'log',
            'yscale': 'log'
        }
        
    elif stat_name in ['fGas', 'fGas_2p']:
        return {
            'title': 'Cluster gas fraction',
            'xlabel': r"$M_{\mathrm{500c}} / h^{-1}\mathrm{M}_{\odot}$",
            'ylabel': r"$M_{\mathrm{gas}} / M_{\mathrm{500c}} \quad [<R_{\mathrm{500c}}]$",
            'xscale': 'log',
            'yscale': 'log'
        }
        
    elif stat_name in ['CGD', 'CGD_2p']:
        return {
            'title': 'Cluster gas density',
            'xlabel': r"$r/R_{\mathrm{500c}}$",
            'ylabel': r"$\rho_{\mathrm{gas}} \,/\, \rho_{\mathrm{crit}}$",
            'xscale': 'log',
            'yscale': 'log'
        }
        
    elif stat_name == 'Pk':
        return {
            'title': 'Total power spectra ratio',
            'xlabel': r'$k \, [h\,\mathrm{Mpc}^{-1}]$',
            'ylabel': r'$P_{\mathrm{sub}}(k)\,/\,P_{\mathrm{grav}}(k)$',
            'xscale': 'log',
            'yscale': 'linear'
        }
        
    elif stat_name == 'CSFR':
        return {
            'title': 'Cosmic star formation rate',
            'xlabel': r"$a$",
            'ylabel': r"$\mathrm{CSFR} \, [\mathrm{M}_{\odot} \, \mathrm{yr}^{-1} \, (h^{-1}\mathrm{Mpc})^{-3}]$",
            'xscale': 'linear',
            'yscale': 'linear'
        }
        
    else:
        raise ValueError(f"Unknown statistic: {stat_name}")


def get_valid_range(stat_name):
    """
    Get the valid/recommended range for a summary statistic.
    
    This returns the range where the emulator is most reliable,
    based on the training data coverage.
    
    Parameters
    ----------
    stat_name : str
        Name of the summary statistic
        
    Returns
    -------
    tuple
        (min_value, max_value) for the independent variable
        
    Examples
    --------
    >>> min_val, max_val = get_valid_range('GSMF')
    >>> print(f"Valid range: {min_val:.2e} to {max_val:.2e}")
    """
    
    if stat_name == 'GSMF':
        return (5e9, 3e11)
        
    elif stat_name == 'BHMSM':
        return (1e10, 2e12)
        
    elif stat_name in ['fGas', 'fGas_2p']:
        return (10**13.5, 10**14.3)
        
    elif stat_name in ['CGD', 'CGD_2p']:
        return (0.015, 2.75)
        
    elif stat_name == 'Pk':
        return (0.04908738521234052, 12.566370614359172)
        
    elif stat_name == 'CSFR':
        return (0.0, 1.0)
        
    else:
        raise ValueError(f"Unknown statistic: {stat_name}")


def get_parameter_info():
    """
    Get information about the input parameters.
    
    Returns
    -------
    dict
        Dictionary with parameter information including names, ranges, and descriptions
    """
    return {
        'names': [
            'kappa_w',
            'e_w', 
            'M_seed',
            'v_kin',
            'epsilon_kin'
        ],
        'latex_names': [
            r'$\kappa_\text{w}$',
            r'$e_\text{w}$',
            r'$M_\text{seed}/10^{6}$',
            r'$v_\text{kin}/10^{4}$',
            r'$\epsilon_\text{kin}/10^{1}$'
        ],
        'ranges': {
            'kappa_w': (2.0, 4.0),
            'e_w': (0.2, 1.0),
            'M_seed': (0.6, 1.2),  # In units of 10^6 M_sun
            'v_kin': (0.1, 1.2),   # In units of 10^4 km/s
            'epsilon_kin': (0.02, 1.2)  # In units of 10^1
        },
        'descriptions': {
            'kappa_w': 'Wind efficiency parameter',
            'e_w': 'Wind energy fraction',
            'M_seed': 'Black hole seed mass (in 10^6 M_sun)',
            'v_kin': 'Kinetic wind velocity (in 10^4 km/s)',
            'epsilon_kin': 'Kinetic feedback efficiency (in 10^1)'
        },
        'scales': {
            'M_seed': 1e6,
            'v_kin': 1e4,
            'epsilon_kin': 1e1
        }
    }
