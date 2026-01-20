"""Debug SEPIA's handling of 2p models."""

import numpy as np
import pickle
from sepia.SepiaData import SepiaData
from sepia.SepiaModel import SepiaModel
from sepia.SepiaPredict import SepiaEmulatorPrediction

# Load the 2p model data
print("=== Loading fGas_2p data ===")
params = np.load('subgrid_emu/data/fGas_2p_z_index0_params.npy')
y_vals = np.load('subgrid_emu/data/fGas_2p_z_index0_y_vals.npy')
y_ind = np.load('subgrid_emu/data/fGas_2p_z_index0_y_ind.npy')

print(f"params shape: {params.shape}")
print(f"y_vals shape: {y_vals.shape}")
print(f"y_ind shape: {y_ind.shape}")

# Create SEPIA data
sepia_data = SepiaData(t_sim=params, y_sim=y_vals, y_ind_sim=y_ind)
print(f"\nSepiaData created")
print(f"  sim_data.x shape: {sepia_data.sim_data.x.shape if hasattr(sepia_data.sim_data, 'x') else 'No x'}")
print(f"  sim_data.t shape: {sepia_data.sim_data.t.shape if hasattr(sepia_data.sim_data, 't') else 'No t'}")

# Do PCA
sepia_data.transform_xt()
sepia_data.standardize_y()
sepia_data.create_K_basis(n_pc=0.99)
print(f"\nAfter PCA:")
print(f"  K shape: {sepia_data.sim_data.K.shape}")
print(f"  Number of PC components: {sepia_data.sim_data.K.shape[1]}")

# Create model
sepia_model = SepiaModel(sepia_data)
print(f"\nSepiaModel created")

# Load the saved model
model_path = 'subgrid_emu/models/fGas_2p_multivariate_model_z_index0.pkl'
with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

print(f"\nModel data keys: {list(model_data.keys())}")
if 'samples' in model_data:
    samples = model_data['samples']
    print(f"Sample keys: {list(samples.keys())}")
    if 'betaU' in samples:
        betaU = samples['betaU']
        print(f"betaU shape: {betaU.shape}")
        print(f"betaU[-1] shape: {betaU[-1].shape}")
        print(f"betaU[-1] flattened shape: {betaU[-1].flatten().shape}")

# Now let's trace what SEPIA expects
print("\n=== What SEPIA expects in wPred ===")
print("In wPred, SEPIA does:")
print("  p = model.data.sim_data.x.shape[1]  # number of simulation parameters")
print("  q = 1 if model has observational data else 0")
print("  pu = model.data.sim_data.K.shape[1]  # number of PC components")
print("  betaU = samples['betaU'][-1].flatten()")
print("  betaU = np.reshape(betaU, (p+q, pu), order='F')")

# Calculate expected values
p = 2  # 2 parameters for 2p models
q = 0  # No observational data (based on the notebook)
pu = sepia_data.sim_data.K.shape[1]

print(f"\nExpected reshape:")
print(f"  p = {p}")
print(f"  q = {q}")
print(f"  pu = {pu}")
print(f"  Expected shape: ({p+q}, {pu})")
print(f"  betaU size: {betaU[-1].size}")
print(f"  Can reshape? {betaU[-1].size == (p+q)*pu}")

# The issue seems to be that betaU has shape (3, n_pc) instead of (2, n_pc)
# This suggests q=1 was used during training
print("\n=== Hypothesis: q=1 was used during training ===")
q_train = 1
print(f"If q=1 during training:")
print(f"  Expected shape during training: ({p+q_train}, {pu}) = ({p+q_train}, {pu})")
print(f"  betaU actual shape: {betaU[-1].shape}")
print(f"  Match? {betaU[-1].shape == (p+q_train, pu)}")
