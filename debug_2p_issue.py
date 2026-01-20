"""Debug script to understand the 2p emulator reshape issue."""

import numpy as np
import pickle
import sys
from io import StringIO

# Test CGD_2p
print("=== Testing CGD_2p ===")
print("Data shapes:")
print(f"  params: (64, 2)")
print(f"  y_vals: (64, 19)")
print(f"  y_ind: (19,)")

# Load the model to inspect its structure
model_path = "subgrid_emu/models/CGD_2p_multivariate_model_z_index0.pkl"
try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    print("\nModel structure:")
    print(f"  Keys: {list(model_data.keys())}")
    
    if 'samples' in model_data:
        samples = model_data['samples']
        print(f"\n  Sample keys: {list(samples.keys())}")
        
        # Check betaU shape
        if 'betaU' in samples:
            betaU = samples['betaU']
            print(f"  betaU shape: {betaU.shape}")
            print(f"  betaU last sample shape: {betaU[-1].shape if len(betaU.shape) > 1 else 'scalar'}")
    
    if 'param_info' in model_data:
        param_info = model_data['param_info']
        if 'betaU' in param_info:
            print(f"\n  betaU param info: {param_info['betaU']}")
            
except Exception as e:
    print(f"Error loading model: {e}")

print("\n=== Testing fGas_2p ===")
print("Data shapes:")
print(f"  params: (64, 2)")
print(f"  y_vals: (64, 8)")
print(f"  y_ind: (8,)")

# Load the fGas_2p model
model_path = "subgrid_emu/models/fGas_2p_multivariate_model_z_index0.pkl"
try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    if 'samples' in model_data:
        samples = model_data['samples']
        if 'betaU' in samples:
            betaU = samples['betaU']
            print(f"\nfGas_2p betaU shape: {betaU.shape}")
            
except Exception as e:
    print(f"Error loading fGas_2p model: {e}")

# Now let's trace through what SEPIA is trying to do
print("\n=== Understanding SEPIA reshape ===")
print("The error occurs in SepiaPredict.py line 475:")
print("  betaU=np.reshape(betaU,(p+q,pu),order='F')")
print("\nWhere:")
print("  p = number of simulation parameters (2 for 2p models)")
print("  q = number of observational parameters (typically 1)")
print("  pu = number of PC basis functions")
print("\nThe error suggests:")
print("  - For CGD_2p: trying to reshape array of size 6 into shape (3,4)")
print("    This means p+q=3, pu=4, but betaU has 6 elements")
print("  - For fGas_2p: trying to reshape array of size 12 into shape (3,7)")
print("    This means p+q=3, pu=7, but betaU has 12 elements")
