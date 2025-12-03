"""
Extract and save Pk_2p training data from the 256MPC 2-parameter runs.
Based on the notebook: Flamingo/Clean/gp_HACC_emu_pk256.ipynb
"""

import numpy as np
import os
import sys
import re

# Add the hydro_emu module to path
sys.path.insert(0, '../../Flamingo/Clean')

from hydro_emu.load_hacc2p import read_pk, vkin_scale, eps_scale

# Configuration from the notebook
DirIn = '../../Data/ProfileData/SCIDAC_RUNS/256MPC_RUNS_HACC_2PARAM_Pk/'
num_sims = 16
z_index = 0

# Pattern for VKIN and EPS
pattern = re.compile(r'VKIN_(\d+\.?\d*)_EPS_(\d+\.?\d*)')

def read_params_from_files(pattern):
    data = []
    for subdirectory_name in os.listdir(DirIn):
        match = pattern.match(subdirectory_name)
        if match:
            data.append([float(match.group(1)), float(match.group(2))])
        else:
            print(f"No match: {subdirectory_name}")
    params_all = np.array(data)
    return params_all

def main():
    print("Extracting Pk_2p training data...")
    print(f"Reading from: {DirIn}\n")
    
    # Read parameters
    params = read_params_from_files(pattern)
    
    # Scale parameters
    params[:, 0] = params[:, 0] / vkin_scale
    params[:, 1] = params[:, 1] / eps_scale
    
    print(f"Found {params.shape[0]} simulations")
    print(f"Parameters shape: {params.shape}")
    
    # Read Pk data
    k, pk_all, pk_ratio = read_pk(DirIn, num_sims, params)
    
    # Apply k limits from notebook
    mlim1 = 0.04908738521234052  # From notebook: 0.5 * 0.02454369260617026
    mlim2 = 12.566370614359172
    
    # Apply mass condition
    mass_cond = np.where((k > mlim1) & (k < mlim2))
    
    # Extract training data
    y_vals = pk_ratio[:, mass_cond][:, 0, :]
    y_ind = k[mass_cond]
    
    # Save training data
    output_dir = '../subgrid_emu/data'
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = f"Pk_2p_z_index{z_index}"
    np.save(os.path.join(output_dir, f"{base_name}_params.npy"), params)
    np.save(os.path.join(output_dir, f"{base_name}_y_vals.npy"), y_vals)
    np.save(os.path.join(output_dir, f"{base_name}_y_ind.npy"), y_ind)
    
    print(f"\n✓ Saved Pk_2p training data:")
    print(f"    params: {params.shape}")
    print(f"    y_vals: {y_vals.shape}")
    print(f"    y_ind: {y_ind.shape}")
    print(f"    k range: {y_ind.min():.6f} to {y_ind.max():.6f}")
    print(f"\nData saved to: {output_dir}")

if __name__ == "__main__":
    main()
