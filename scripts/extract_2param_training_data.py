"""
Extract training data for 2-parameter models from 256MPC runs.
These models use a different dataset with only v_kin and epsilon_kin parameters.
"""

import numpy as np
import os
import sys
import re

# Add the hydro_emu module to path
sys.path.insert(0, '../../Flamingo/Clean')

from hydro_emu.load_hacc import (
    read_cgd, read_gasfr, mass_conds
)

# Configuration for 256MPC 2-parameter runs
DirIn256 = '../../Data/ProfileData/SCIDAC_RUNS/256MPC_2PARAM/EXTRACT_DATA/'
num_sims256 = 16
z_index = 0

# Scaling factors
vkin_scale = 1e4
eps_scale = 1e1

def read_params_from_files_256():
    """Read 2 parameters from 256MPC simulation files"""
    pattern = re.compile(r'VKIN_(\d+\.?\d*)_EPS_(\d+\.?\d*)')
    
    data = []
    for subdirectory_name in os.listdir(DirIn256):
        match = pattern.match(subdirectory_name)
        if match:
            data.append([
                float(match.group(1)),
                float(match.group(2))
            ])
    
    return np.array(data)

def save_training_data_for_stat(stat_name, params, y_vals, y_ind, z_index=0):
    """Save training data for a specific statistic"""
    output_dir = '../subgrid_emu/data'
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = f"{stat_name}_z_index{z_index}"
    np.save(os.path.join(output_dir, f"{base_name}_params.npy"), params)
    np.save(os.path.join(output_dir, f"{base_name}_y_vals.npy"), y_vals)
    np.save(os.path.join(output_dir, f"{base_name}_y_ind.npy"), y_ind)
    
    print(f"✓ Saved {stat_name}:")
    print(f"    params: {params.shape}")
    print(f"    y_vals: {y_vals.shape}")
    print(f"    y_ind: {y_ind.shape}")

def main():
    print("Extracting 2-parameter training data from 256MPC runs...")
    print(f"Reading from: {DirIn256}\n")
    
    # Read 2 parameters (v_kin, epsilon_kin)
    params256 = read_params_from_files_256()
    params256[:, 0] = params256[:, 0] / vkin_scale
    params256[:, 1] = params256[:, 1] / eps_scale
    print(f"Parameters shape: {params256.shape} (2-parameter model)\n")
    
    # CGD_2p - use standard read_cgd function with 256MPC directory
    print("Processing CGD_2p...")
    radius256, cgd_arr256 = read_cgd(DirIn256, num_sims256, params256)
    rlim1, rlim2 = mass_conds('CGD')
    rad_cond_256 = np.where((radius256 > rlim1) & (radius256 < rlim2))
    y_vals_cgd_256 = cgd_arr256[:, rad_cond_256][:, 0, :]
    y_ind_cgd_256 = radius256[rad_cond_256]
    save_training_data_for_stat('CGD_2p', params256, y_vals_cgd_256, y_ind_cgd_256, z_index)
    
    # CGD_CC_2p - same as CGD_2p (Cool Core variant uses same data structure)
    print("Processing CGD_CC_2p...")
    save_training_data_for_stat('CGD_CC_2p', params256, y_vals_cgd_256, y_ind_cgd_256, z_index)
    
    # fGas_2p - use standard read_gasfr function with 256MPC directory
    print("Processing fGas_2p...")
    log_halo_mass256, gas_fr_arr256 = read_gasfr(DirIn256, num_sims256, params256)
    mlim1, mlim2 = mass_conds('fGas')
    mass_cond_256 = np.where((10**log_halo_mass256 > mlim1) & (10**log_halo_mass256 < mlim2))
    y_vals_fgas_256 = gas_fr_arr256[:, mass_cond_256][:, 0, :]
    y_ind_fgas_256 = 10**log_halo_mass256[mass_cond_256]
    save_training_data_for_stat('fGas_2p', params256, y_vals_fgas_256, y_ind_fgas_256, z_index)
    
    print("\n✓ All 2-parameter training data saved successfully!")
    print(f"Data saved to: subgrid_emu/data/")

if __name__ == "__main__":
    main()
