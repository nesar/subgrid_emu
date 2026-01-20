"""
Create a workaround for 2p models by understanding their structure.

The issue is that 2p models were trained with observational data,
creating an extra dimension in betaU. We need to handle this specially.
"""

import numpy as np
import pickle
import os

def analyze_2p_models():
    """Analyze all 2p models to understand their structure."""
    
    models_dir = 'subgrid_emu/models/'
    data_dir = 'subgrid_emu/data/'
    
    for stat_name in ['CGD_2p', 'fGas_2p', 'Pk_2p']:
        print(f"\n=== Analyzing {stat_name} ===")
        
        # Load model
        model_path = os.path.join(models_dir, f'{stat_name}_multivariate_model_z_index0.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            if 'samples' in model_data and 'betaU' in model_data['samples']:
                betaU = model_data['samples']['betaU']
                print(f"  Model betaU shape: {betaU.shape}")
                print(f"  Last sample shape: {betaU[-1].shape}")
        
        # Load data
        params_path = os.path.join(data_dir, f'{stat_name}_z_index0_params.npy')
        y_vals_path = os.path.join(data_dir, f'{stat_name}_z_index0_y_vals.npy')
        y_ind_path = os.path.join(data_dir, f'{stat_name}_z_index0_y_ind.npy')
        
        if all(os.path.exists(p) for p in [params_path, y_vals_path, y_ind_path]):
            params = np.load(params_path)
            y_vals = np.load(y_vals_path)
            y_ind = np.load(y_ind_path)
            
            print(f"  Data shapes:")
            print(f"    params: {params.shape}")
            print(f"    y_vals: {y_vals.shape}")
            print(f"    y_ind: {y_ind.shape}")

def create_workaround_script():
    """Create a script that properly handles 2p models."""
    
    workaround_code = '''"""
Workaround for 2p model issues in subgrid_emu.

The 2p models were trained with observational data included, which creates
a mismatch in the betaU dimensions. This script provides a fix.
"""

import numpy as np
from sepia.SepiaData import SepiaData
from sepia.SepiaModel import SepiaModel
import pickle
import os

def load_2p_model_with_obs_data(stat_name, z_index=0):
    """
    Load a 2p model with the correct observational data structure.
    
    The key insight is that 2p models were trained with observational data,
    so we need to create dummy observational data when loading them.
    """
    # Load the training data
    data_dir = 'subgrid_emu/data'
    base_name = f"{stat_name}_z_index{z_index}"
    
    params = np.load(os.path.join(data_dir, f"{base_name}_params.npy"))
    y_vals = np.load(os.path.join(data_dir, f"{base_name}_y_vals.npy"))
    y_ind = np.load(os.path.join(data_dir, f"{base_name}_y_ind.npy"))
    
    # Create dummy observational data
    # The 2p models expect observational data with 1 extra dimension
    n_obs = y_vals.shape[1]  # Number of y values
    
    # Create dummy observational data (zeros with small noise)
    y_obs = np.zeros(n_obs) + np.random.normal(0, 0.01, n_obs)
    x_obs = np.array([[0.5]])  # Single observational parameter
    
    # Create SepiaData with observational data
    sepia_data = SepiaData(
        t_sim=params,
        y_sim=y_vals,
        y_ind_sim=y_ind,
        x_obs=x_obs,
        y_obs=y_obs,
        y_ind_obs=y_ind
    )
    
    # Do PCA
    sepia_data.transform_xt()
    sepia_data.standardize_y()
    
    # Use the correct explained variance for 2p models
    exp_variance = 0.99
    if stat_name == 'Pk_2p':
        exp_variance = 0.9999
    
    sepia_data.create_K_basis(n_pc=exp_variance)
    
    # Create model
    sepia_model = SepiaModel(sepia_data)
    
    # Load the saved parameters
    model_path = f'subgrid_emu/models/{stat_name}_multivariate_model_z_index{z_index}'
    sepia_model.restore_model_info(model_path)
    
    return sepia_model

# Test the workaround
if __name__ == "__main__":
    for stat_name in ['CGD_2p', 'fGas_2p', 'Pk_2p']:
        try:
            model = load_2p_model_with_obs_data(stat_name)
            print(f"✓ Successfully loaded {stat_name}")
            
            # Test prediction
            params = np.array([[0.65, 0.1]])
            samples = model.get_samples(numsamples=1)
            
            from sepia.SepiaPredict import SepiaEmulatorPrediction
            pred = SepiaEmulatorPrediction(
                t_pred=params,
                samples=samples,
                model=model,
                storeMuSigma=True
            )
            
            print(f"  Prediction successful!")
            
        except Exception as e:
            print(f"✗ Failed to load {stat_name}: {e}")
'''
    
    with open('subgrid_emu/workaround_2p_models.py', 'w') as f:
        f.write(workaround_code)
    
    print("Created workaround_2p_models.py")

if __name__ == "__main__":
    analyze_2p_models()
    create_workaround_script()
