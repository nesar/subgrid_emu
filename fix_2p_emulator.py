"""
Fix for 2p emulator issues in subgrid_emu package.

The issue is that 2p models were trained with a different SEPIA configuration
where betaU has shape (3, n_pc) instead of (p+q, n_pc) where p=2, q=1.
This suggests the models might have been trained with q=1 (observational parameter)
or with a different parameter structure.
"""

import numpy as np
from sepia.SepiaPredict import SepiaEmulatorPrediction, wPred
import sepia.SepiaPredict

# Create a patched version of wPred that handles 2p models correctly
def wPred_patched(sepPred):
    """
    Patched version of SEPIA's wPred function that handles 2p models correctly.
    """
    # Get the original function
    import inspect
    original_code = inspect.getsource(wPred)
    
    # The issue is in line 475 of the original:
    # betaU=np.reshape(betaU,(p+q,pu),order='F')
    
    # For 2p models, betaU already has the correct shape (3, n_pc)
    # We need to detect this and handle it differently
    
    # Call the original function but wrap the problematic reshape
    model = sepPred.model
    samples = sepPred.samples
    
    # Check if this is a 2p model
    if hasattr(model.data.sim_data, 'x') and model.data.sim_data.x.shape[1] == 2:
        # This is a 2p model
        # Get betaU from samples
        if 'betaU' in samples:
            betaU_samples = samples['betaU']
            if len(betaU_samples.shape) == 3 and betaU_samples.shape[1] == 3:
                # This is the problematic case - betaU has shape (n_samples, 3, n_pc)
                # We need to handle this specially
                
                # Temporarily modify the samples to have the expected shape
                # The original code expects betaU to be flattened
                n_samples = betaU_samples.shape[0]
                n_pc = betaU_samples.shape[2]
                
                # Flatten betaU for the reshape operation
                samples_copy = samples.copy()
                samples_copy['betaU'] = betaU_samples.reshape(n_samples, -1)
                
                # Update sepPred.samples temporarily
                original_samples = sepPred.samples
                sepPred.samples = samples_copy
                
                try:
                    # Call original wPred
                    wPred(sepPred)
                finally:
                    # Restore original samples
                    sepPred.samples = original_samples
                
                return
    
    # For all other cases, call the original function
    wPred(sepPred)


# Monkey patch the function
sepia.SepiaPredict.wPred = wPred_patched


def test_2p_fix():
    """Test that the fix works for 2p models."""
    from subgrid_emu import load_emulator
    
    print("Testing 2p emulator fix...")
    
    # Test CGD_2p
    try:
        emu = load_emulator('CGD_2p')
        params = [0.65, 0.1]
        mean, std = emu.predict(params)
        print(f"✓ CGD_2p prediction successful: shape={mean.shape}")
    except Exception as e:
        print(f"✗ CGD_2p failed: {e}")
    
    # Test fGas_2p
    try:
        emu = load_emulator('fGas_2p')
        params = [0.65, 0.1]
        mean, std = emu.predict(params)
        print(f"✓ fGas_2p prediction successful: shape={mean.shape}")
    except Exception as e:
        print(f"✗ fGas_2p failed: {e}")
    
    # Test Pk_2p
    try:
        emu = load_emulator('Pk_2p')
        params = [0.65, 0.1]
        mean, std = emu.predict(params)
        print(f"✓ Pk_2p prediction successful: shape={mean.shape}")
    except Exception as e:
        print(f"✗ Pk_2p failed: {e}")
    
    print("\nFix testing complete!")


if __name__ == "__main__":
    test_2p_fix()
