"""
Extract training data from the Flamingo/Clean notebook setup and save it.
This script replicates the data loading from final_compare_frontierE.ipynb
"""

import numpy as np
import os
import sys

# Add the hydro_emu module to path
sys.path.insert(0, '../../Flamingo/Clean')

from hydro_emu.load_hacc import (
    read_gsmf, read_bhmsm, read_gasfr, read_cged, read_cgd,
    fill_nan_with_interpolation, mass_conds
)

# Configuration
DirIn = '../../Data/ProfileData/SCIDAC_RUNS/128MPC_RUNS_HACC_5PARAM_extract2/'
num_sims = 64
z_index = 0

# Scaling factors
seed_mass_scale = 1e6
vkin_scale = 1e4
eps_scale = 1e1

def read_params_from_files(dir_in):
    """Read parameters from simulation files"""
    import re
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
    print("Extracting training data from simulation files...")
    print(f"Reading from: {DirIn}\n")
    
    # Read parameters
    params = read_params_from_files(DirIn)
    params[:, 2] = params[:, 2] / seed_mass_scale
    params[:, 3] = params[:, 3] / vkin_scale
    params[:, 4] = params[:, 4] / eps_scale
    print(f"Parameters shape: {params.shape}\n")
    
    # GSMF
    print("Processing GSMF...")
    stellar_mass, gsmf_arr = read_gsmf(DirIn, num_sims, params)
    gsmf_arr_filled = fill_nan_with_interpolation(gsmf_arr, 'linear')
    mlim1, mlim2 = mass_conds('GSMF')
    mass_cond = np.where((stellar_mass > mlim1) & (stellar_mass < mlim2))
    y_vals_gsmf = 10**gsmf_arr_filled[:, mass_cond][:, 0, :]
    y_ind_gsmf = stellar_mass[mass_cond]
    save_training_data_for_stat('GSMF', params, y_vals_gsmf, y_ind_gsmf, z_index)
    
    # BHMSM
    print("Processing BHMSM...")
    log_bhmsm_mass, bhmsm_arr = read_bhmsm(DirIn, num_sims, params)
    bhmsm_arr_filled = fill_nan_with_interpolation(bhmsm_arr, 'cubic')
    mlim1, mlim2 = mass_conds('BHMSM')
    mass_cond = np.where((10**log_bhmsm_mass > mlim1) & (10**log_bhmsm_mass < mlim2))
    y_vals_bhmsm = np.log10(bhmsm_arr_filled[:, mass_cond][:, 0, :])
    y_ind_bhmsm = 10**log_bhmsm_mass[mass_cond]
    save_training_data_for_stat('BHMSM', params, y_vals_bhmsm, y_ind_bhmsm, z_index)
    
    # fGas
    print("Processing fGas...")
    log_halo_mass, gas_fr_arr = read_gasfr(DirIn, num_sims, params)
    gas_fr_arr_filled = fill_nan_with_interpolation(gas_fr_arr, 'cubic')
    mlim1, mlim2 = mass_conds('fGas')
    mass_cond = np.where((10**log_halo_mass > mlim1) & (10**log_halo_mass < mlim2))
    y_vals_fgas = gas_fr_arr_filled[:, mass_cond][:, 0, :]
    y_ind_fgas = 10**log_halo_mass[mass_cond]
    save_training_data_for_stat('fGas', params, y_vals_fgas, y_ind_fgas, z_index)
    
    # CGD
    print("Processing CGD...")
    radius, cgd_arr = read_cgd(DirIn, num_sims, params)
    rlim1, rlim2 = mass_conds('CGD')
    rad_cond = np.where((radius > rlim1) & (radius < rlim2))
    y_vals_cgd = cgd_arr[:, rad_cond][:, 0, :]
    y_ind_cgd = radius[rad_cond]
    save_training_data_for_stat('CGD', params, y_vals_cgd, y_ind_cgd, z_index)
    
    # CGED
    print("Processing CGED...")
    radius, cged_arr = read_cged(DirIn, num_sims, params)
    rlim1, rlim2 = mass_conds('CGED')
    rad_cond = np.where((radius > rlim1) & (radius < rlim2))
    y_vals_cged = cged_arr[:, rad_cond][:, 0, :]
    y_ind_cged = radius[rad_cond]
    save_training_data_for_stat('CGED', params, y_vals_cged, y_ind_cged, z_index)
    
    # 2-parameter models - use only last 2 parameters (v_kin, epsilon_kin)
    params_2p = params[:, 3:5]  # Extract only v_kin and epsilon_kin
    
    # CGD_2p - same data as CGD but with 2 parameters
    print("Processing CGD_2p...")
    save_training_data_for_stat('CGD_2p', params_2p, y_vals_cgd, y_ind_cgd, z_index)
    
    # fGas_2p - same data as fGas but with 2 parameters
    print("Processing fGas_2p...")
    save_training_data_for_stat('fGas_2p', params_2p, y_vals_fgas, y_ind_fgas, z_index)
    
    # CGD_CC_2p - same as CGD_2p (Cool Core variant uses same structure)
    print("Processing CGD_CC_2p...")
    save_training_data_for_stat('CGD_CC_2p', params_2p, y_vals_cgd, y_ind_cgd, z_index)
    
    print("\n✓ All training data saved successfully!")
    print(f"Data saved to: subgrid_emu/data/")

if __name__ == "__main__":
    main()
