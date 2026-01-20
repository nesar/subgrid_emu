"""
Subgrid Physics Emulator

This module provides a clean interface for loading and using trained emulators
for various cosmological summary statistics.
"""

import numpy as np
import os
import sys
import warnings
from io import StringIO
try:
    # Python 3.9+
    from importlib.resources import files
except ImportError:
    # Fallback for older Python versions
    from importlib_resources import files
from sepia.SepiaModel import SepiaModel
from sepia.SepiaData import SepiaData
from sepia.SepiaPredict import SepiaEmulatorPrediction
from .model_metadata import get_training_grid

# No patch needed - we'll handle 2p models differently


# Physical parameter scaling factors
SEED_MASS_SCALE = 1e6
VKIN_SCALE = 1e4
EPS_SCALE = 1e1

# Parameter names for display
PARAM_NAMES = [
    r'$\kappa_\text{w}$', 
    r'$e_\text{w}$', 
    r'$M_\text{seed}/10^{6}$', 
    r'$v_\text{kin}/10^{4}$', 
    r'$\epsilon_\text{kin}/10^{1}$'
]

# Available summary statistics
# AVAILABLE_STATS_5P = ['GSMF', 'BHMSM', 'fGas', 'CGD', 'Pk', 'CSFR']
AVAILABLE_STATS_5P = ['GSMF', 'CGD', 'fGas', 'BHMSM', 'CSFR', 'Pk']
AVAILABLE_STATS_2P = ['CGD_2p', 'fGas_2p', 'Pk_2p']


def get_model_path(stat_name, z_index=0):
    """
    Get the path to a trained model file.
    
    Parameters
    ----------
    stat_name : str
        Name of the summary statistic (e.g., 'GSMF', 'fGas', 'CGD')
    z_index : int, optional
        Redshift index (default: 0 for z=0)
        
    Returns
    -------
    str
        Full path to the model file
    """
    model_filename = f"{stat_name}_multivariate_model_z_index{z_index}.pkl"
    
    try:
        # Try to get from installed package using importlib.resources
        package_files = files('subgrid_emu')
        model_path = str(package_files / 'models' / model_filename)
    except:
        # Fallback to relative path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'models', model_filename)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found: {model_path}\n"
            f"Available statistics: {AVAILABLE_STATS_5P + AVAILABLE_STATS_2P}"
        )
    
    return model_path


def _do_pca(sepia_data, exp_variance=0.99):
    """
    Perform PCA on SEPIA data and create model.
    
    Parameters
    ----------
    sepia_data : SepiaData
        Input data in SEPIA format
    exp_variance : float
        Explained variance threshold (default: 0.99)
        
    Returns
    -------
    SepiaModel
        SEPIA model after PCA
    """
    sepia_data.transform_xt()
    sepia_data.standardize_y()
    sepia_data.create_K_basis(n_pc=exp_variance)
    sepia_model = SepiaModel(sepia_data)
    return sepia_model


def _sepia_data_format(design, y_vals, y_ind):
    """
    Format data for SEPIA.
    
    Parameters
    ----------
    design : np.array
        Parameter array of shape (num_simulation, num_params)
    y_vals : np.array
        Target values of shape (num_simulation, num_y_values)
    y_ind : np.array
        Independent variable values of shape (num_y_values,)
        
    Returns
    -------
    SepiaData
        Formatted SEPIA data
    """
    return SepiaData(t_sim=design, y_sim=y_vals, y_ind_sim=y_ind)


class SubgridEmulator:
    """
    Main emulator class for making predictions.
    
    This class loads trained emulator models and provides methods for
    making predictions of various cosmological summary statistics.
    
    Parameters
    ----------
    stat_name : str
        Name of the summary statistic to emulate
    z_index : int, optional
        Redshift index (default: 0)
    exp_variance : float, optional
        Explained variance for PCA (default: 0.95 for 5-param, 0.99 for 2-param)
        
    Attributes
    ----------
    stat_name : str
        Name of the loaded statistic
    model : SepiaModel
        Loaded SEPIA model
    n_params : int
        Number of input parameters (5 or 2)
    """
    
    def __init__(self, stat_name, z_index=0, exp_variance=None):
        self.stat_name = stat_name
        self.z_index = z_index
        
        # Check if statistic is available
        if stat_name not in AVAILABLE_STATS_2P + AVAILABLE_STATS_5P:
            raise ValueError(
                f"Unknown statistic: {stat_name}\n"
                f"Available: {AVAILABLE_STATS_5P + AVAILABLE_STATS_2P}"
            )
        
        # Get metadata from model_metadata.py
        try:
            metadata = get_training_grid(stat_name)
            self.n_params = metadata['n_params']
            # Use provided exp_variance or default from metadata
            self.exp_variance = exp_variance if exp_variance is not None else metadata['exp_variance']
        except ValueError:
            # Fallback for statistics not in metadata (shouldn't happen for standard stats)
            if stat_name in AVAILABLE_STATS_2P:
                self.n_params = 2
                self.exp_variance = exp_variance if exp_variance is not None else 0.99
            else:
                self.n_params = 5
                self.exp_variance = exp_variance if exp_variance is not None else 0.95
        
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model from disk."""
        model_path = get_model_path(self.stat_name, self.z_index)
        
        # Load the training data that was used to create this model
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        base_name = f"{self.stat_name}_z_index{self.z_index}"
        
        params_path = os.path.join(data_dir, f"{base_name}_params.npy")
        y_vals_path = os.path.join(data_dir, f"{base_name}_y_vals.npy")
        y_ind_path = os.path.join(data_dir, f"{base_name}_y_ind.npy")
        
        # Check if training data exists
        if not all(os.path.exists(p) for p in [params_path, y_vals_path, y_ind_path]):
            raise FileNotFoundError(
                f"Training data not found for {self.stat_name}. "
                f"Expected files in {data_dir}:\n"
                f"  - {base_name}_params.npy\n"
                f"  - {base_name}_y_vals.npy\n"
                f"  - {base_name}_y_ind.npy"
            )
        
        # Load training data
        params = np.load(params_path)
        y_vals = np.load(y_vals_path)
        y_ind = np.load(y_ind_path)
        
        # Special handling for 2p models - they were trained with observational data
        if self.stat_name in AVAILABLE_STATS_2P:
            # Create dummy observational data to match training structure
            n_obs = y_vals.shape[1]  # Number of y values
            n_sim = params.shape[0]
            
            # Create dummy x_sim (single column of zeros)
            x_sim = np.zeros((n_sim, 1))
            
            # Create dummy observational data - single observation
            # Reshape y_obs to be (1, n_obs) to match x_obs shape (1, 1)
            y_obs = np.mean(y_vals, axis=0).reshape(1, -1)
            x_obs = np.array([[0.5]])  # Single observational parameter
            
            # Create SepiaData with both x_sim and x_obs
            sepia_data = SepiaData(
                x_sim=x_sim,
                t_sim=params,
                y_sim=y_vals,
                y_ind_sim=y_ind,
                x_obs=x_obs,
                y_obs=y_obs,
                y_ind_obs=y_ind
            )
        else:
            # Create SepiaData normally for 5p models
            sepia_data = _sepia_data_format(params, y_vals, y_ind)
        
        # Perform PCA (this recreates the basis used during training)
        sepia_model = _do_pca(sepia_data, exp_variance=self.exp_variance)
        
        # Load the trained model parameters
        # restore_model_info expects the path without the .pkl extension
        model_path_base = model_path.replace('.pkl', '')
        
        # Use the standard SEPIA restore method
        # This works for all models when the PCA is done with the correct exp_variance
        # Suppress the warning about model instantiation (SEPIA uses print, not warnings)
        try:
            # Redirect stdout to suppress print statements
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                sepia_model.restore_model_info(model_path_base)
            finally:
                sys.stdout = old_stdout
        except IndexError as e:
            # If we get an IndexError during restore (SEPIA bug with single PCA component),
            # manually load the model parameters
            import pickle
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            samples = model_data['samples']
            param_info = model_data['param_info']
            
            # Restore parameter information (excluding logPost)
            for p in sepia_model.params:
                if p.name in param_info and p.name != 'logPost':
                    info = param_info[p.name]
                    p.fixed = info['fixed']
                    p.prior.bounds = info['prior_bounds']
                    p.prior.fcon = info['prior_fcon']
                    p.prior.dist = info['prior_dist']
                    p.prior.params = info['prior_params']
                    p.mcmc.stepParam = info['mcmc_stepParam']
                    p.mcmc.stepType = info['mcmc_stepType']
            
            # Put samples and current values back
            for p in sepia_model.params:
                if p.name in samples:
                    p.val = np.take(samples[p.name], -1, axis=0)
                    draws = [s for s in samples[p.name]]
                    p.mcmc.draws = draws

        self.model = sepia_model

        # Cache constant values for fast predictions
        self._cache_prediction_constants()

    def _cache_prediction_constants(self):
        """Cache constant values used in predictions for performance."""
        self._K = self.model.data.sim_data.K
        self._K_T = self._K.T
        self._y_sd = self.model.data.sim_data.orig_y_sd
        self._y_mean = self.model.data.sim_data.orig_y_mean
        # Cache one posterior sample (minimal since we use mu/Sigma directly)
        self._pred_samples = self.model.get_samples(numsamples=1)

    def predict(self, params):
        """
        Make predictions for given parameters.

        Parameters
        ----------
        params : np.array
            Input parameters. Can be:
            - 1D array of shape (n_params,) for single prediction
            - 2D array of shape (n_pred, n_params) for multiple predictions
            For 5-parameter models: [kappa, e_gw, seed_mass, vkin, eps]
            For 2-parameter models: [vkin, eps]
            Note: Parameters should be in scaled units (see PARAM_NAMES)

        Returns
        -------
        pred_mean : np.array
            Mean prediction (with appropriate scaling applied)
        pred_std : np.array
            Standard deviation for uncertainty (with appropriate scaling applied)

        Notes
        -----
        The predictions are automatically transformed to the correct physical units:
        - GSMF: Transformed to log10 space using delta method
        - BHMSM: Transformed from log10 to linear space (10**) using delta method
        - Other statistics: Returned as-is

        Examples
        --------
        >>> emu = SubgridEmulator('GSMF')
        >>> params = np.array([3.0, 0.5, 0.8, 0.65, 0.1])
        >>> mean, std = emu.predict(params)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call _load_model() first.")

        # Ensure params is 2D
        params = np.atleast_2d(params)

        if params.shape[1] != self.n_params:
            raise ValueError(
                f"Expected {self.n_params} parameters, got {params.shape[1]}"
            )

        # Make prediction with mu and Sigma (using cached samples)
        pred = SepiaEmulatorPrediction(
            t_pred=params,
            samples=self._pred_samples,
            model=self.model,
            storeMuSigma=True
        )

        means = []
        stds = []

        for i in range(params.shape[0]):
            mu = pred.mu[i]            # shape [r]
            Sigma = pred.sigma[i]      # shape [r, r]

            y_mu = self._K_T @ mu                            # shape [p]
            y_cov = self._K_T @ Sigma @ self._K              # shape [p, p]
            y_std = np.sqrt(np.clip(np.diag(y_cov), 0, None))

            # Scale back to original space using cached values
            y_mu = self._y_sd * y_mu + self._y_mean
            y_std = self._y_sd * y_std

            means.append(y_mu)
            stds.append(y_std)

        pred_mean = np.array(means).T  # shape [p, n_pred]
        pred_std = np.array(stds).T    # shape [p, n_pred]

        # Apply output transformations based on statistic type
        # GSMF: emulator outputs linear values, transform to log10 using delta method
        if self.stat_name == 'GSMF':
            # Delta method: for y = log10(x), σ_y = σ_x / (μ_x * ln(10))
            pred_std = pred_std / (pred_mean * np.log(10))
            pred_mean = np.log10(pred_mean)
        # BHMSM: emulator outputs log10 values, transform to linear (10**) using delta method
        elif self.stat_name == 'BHMSM':
            # Delta method: for y = 10^x, σ_y = σ_x * 10^μ_x * ln(10)
            pred_std = pred_std * (10**pred_mean) * np.log(10)
            pred_mean = 10**pred_mean

        # Squeeze to remove extra dimensions for single predictions
        if pred_mean.ndim > 1 and pred_mean.shape[1] == 1:
            pred_mean = pred_mean.squeeze()
            pred_std = pred_std.squeeze()

        return pred_mean, pred_std
    
    def __repr__(self):
        return (
            f"SubgridEmulator(stat_name='{self.stat_name}', "
            f"z_index={self.z_index}, n_params={self.n_params})"
        )


def load_emulator(stat_name, z_index=0, exp_variance=None):
    """
    Convenience function to load an emulator.

    Parameters
    ----------
    stat_name : str
        Name of the summary statistic
    z_index : int, optional
        Redshift index (default: 0)
    exp_variance : float, optional
        Explained variance for PCA

    Returns
    -------
    SubgridEmulator
        Loaded emulator ready for predictions

    Examples
    --------
    >>> emu = load_emulator('GSMF')
    >>> params = [3.0, 0.5, 0.8, 0.65, 0.1]
    >>> mean, std = emu.predict(params)
    """
    return SubgridEmulator(stat_name, z_index, exp_variance)


def list_available_statistics():
    """
    List all available summary statistics.
    
    Returns
    -------
    dict
        Dictionary with '5-parameter' and '2-parameter' keys
    """
    return {
        '5-parameter': AVAILABLE_STATS_5P,
        '2-parameter': AVAILABLE_STATS_2P
    }
