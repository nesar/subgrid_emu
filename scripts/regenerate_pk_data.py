#!/usr/bin/env python3
"""
Regenerate the original Pk training data from simulation files,
then apply the correct mask as used in training.
"""

import numpy as np
import os
import sys
import re

# Add paths
sys.path.insert(0, '/home/nramachandra/Projects/Hydro_runs/Flamingo/Clean')
from hydro_emu.load_hacc import read_pk, mass_conds

# Configuration - from gp_HACC_emu_pk.ipynb
DirIn = '/home/nramachandra/Projects/Hydro_runs/Data/ProfileData/SCIDAC_RUNS/128MPC_RUNS_HACC_5PARAM_extract2_Pk/'
num_sims = 64
z_index = 0

# Scaling factors
seed_mass_scale = 1e6
vkin_scale = 1e4
eps_scale = 1e1

def read_params_from_files(dir_in):
    """Read parameters from simulation files"""
    pattern = re.compile(r'KAPPA_(\d+\.?\d*)_EGW_(\d+\.?\d*)_SEED_([\d\.eE\+\-]+)_VKIN_([\d\.]+)_EPS_([\d\.eE\+\-]+)')
    
    data = []
    for subdirectory_name in os.listdir(dir_in):
        match = pattern.match(subdirectory_name)
        if match:
            data.append([
                float(match.group(1)), 
                float(match.group(2)), 
                float(match.group(3).replace('e', 'E')),
                float(match.group(4)), 
                float(match.group(5).replace('e', 'E'))
            ])
    
    params_all = np.array(data)
    params_all[:, 2] = params_all[:, 2] / seed_mass_scale
    params_all[:, 3] = params_all[:, 3] / vkin_scale
    params_all[:, 4] = params_all[:, 4] / eps_scale
    
    return params_all

print("Regenerating Pk training data...")
print(f"Reading from: {DirIn}\n")

# Read parameters
params = read_params_from_files(DirIn)
print(f"Parameters shape: {params.shape}")

# Read Pk data
k, pk_all, pk_ratio = read_pk(DirIn, num_sims, params)
print(f"Original k shape: {k.shape}")
print(f"Original pk_ratio shape: {pk_ratio.shape}")

# Apply mask EXACTLY as in training
# From gp_HACC_emu_pk.ipynb:
# mlim1, mlim2 = mass_conds('Pk')
# mass_cond = np.where( (k > mlim1)  &  (k < mlim2) )
# y_vals =  pk_ratio[:, mass_cond][:, 0, :]
# y_ind = k[mass_cond]

mlim1, mlim2 = mass_conds('Pk')
print(f"\nApplying mask from mass_conds('Pk'):")
print(f"  mlim1: {mlim1}")
print(f"  mlim2: {mlim2}")

mass_cond = np.where((k > mlim1) & (k < mlim2))
y_vals = pk_ratio[:, mass_cond][:, 0, :]
y_ind = k[mass_cond]

print(f"\nAfter masking:")
print(f"  y_ind shape: {y_ind.shape}")
print(f"  y_vals shape: {y_vals.shape}")

# Save the data
output_dir = '/home/nramachandra/Projects/Hydro_runs/subgrid_emu/subgrid_emu/data'
base_name = f"Pk_z_index{z_index}"

np.save(os.path.join(output_dir, f"{base_name}_params.npy"), params)
np.save(os.path.join(output_dir, f"{base_name}_y_vals.npy"), y_vals)
np.save(os.path.join(output_dir, f"{base_name}_y_ind.npy"), y_ind)

print(f"\n✓ Saved Pk training data:")
print(f"  params: {params.shape}")
print(f"  y_vals: {y_vals.shape}")
print(f"  y_ind: {y_ind.shape}")
print(f"\nData saved to: {output_dir}/")
