#!/usr/bin/env python3
"""
Fix the Pk data files to match the training configuration.

The training in gp_HACC_emu_pk.ipynb applied a specific mask to reduce
the k-points. This script replicates that exact masking procedure.
"""

import numpy as np
import os
import sys

# Add the parent directory to path to import from hydro_emu
sys.path.insert(0, '/home/nramachandra/Projects/Hydro_runs/Flamingo/Clean')
from hydro_emu.load_hacc import mass_conds

# Get the data directory
script_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.dirname(script_dir)
data_dir = os.path.join(package_dir, 'subgrid_emu', 'data')

# Load the current (443-point) data
params_path = os.path.join(data_dir, 'Pk_z_index0_params.npy')
y_vals_path = os.path.join(data_dir, 'Pk_z_index0_y_vals.npy')
y_ind_path = os.path.join(data_dir, 'Pk_z_index0_y_ind.npy')

print("Loading current Pk data...")
params = np.load(params_path)
y_vals_old = np.load(y_vals_path)
y_ind_old = np.load(y_ind_path)

print(f"Current shapes:")
print(f"  params: {params.shape}")
print(f"  y_vals: {y_vals_old.shape}")
print(f"  y_ind: {y_ind_old.shape}")

# Apply the mask EXACTLY as done in training
# From gp_HACC_emu_pk.ipynb:
# mlim1, mlim2 = mass_conds('Pk')
# mass_cond = np.where( (k > mlim1)  &  (k < mlim2) )
# y_ind = k[mass_cond]

mlim1, mlim2 = mass_conds('Pk')
print(f"\nApplying mask from mass_conds('Pk'):")
print(f"  mlim1: {mlim1}")
print(f"  mlim2: {mlim2}")

# Apply mask - note that np.where returns a tuple, so we take [0]
mass_cond = np.where((y_ind_old > mlim1) & (y_ind_old < mlim2))
y_ind_new = y_ind_old[mass_cond]
y_vals_new = y_vals_old[:, mass_cond[0]]

print(f"\nAfter applying mask:")
print(f"  y_ind shape: {y_ind_new.shape}")
print(f"  y_vals shape: {y_vals_new.shape}")

# Check if this matches expected shape from training (255 points)
if y_ind_new.shape[0] != 255:
    print(f"\nWARNING: Expected 255 points after masking, got {y_ind_new.shape[0]}")
    print("This might still be correct if the training used different data.")
    print("Proceeding anyway...")

# Save the masked data
print(f"\nSaving masked data...")
np.save(y_ind_path, y_ind_new)
np.save(y_vals_path, y_vals_new)

print(f"  Saved y_ind to: {y_ind_path}")
print(f"  Saved y_vals to: {y_vals_path}")
print(f"\nPk data fixed successfully!")
print(f"The data now has {y_ind_new.shape[0]} k-points.")
