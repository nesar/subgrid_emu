"""
Script to save training data (p_all, y_vals, y_ind) for each model.
This data is needed to properly load the SEPIA models.

Run this from the Flamingo/Clean directory where the notebook variables are available.
"""

import numpy as np
import os

# This script should be run in an environment where the notebook variables are available
# You can copy the relevant cells from final_compare_frontierE.ipynb

def save_training_data(stat_name, params, y_vals, y_ind, z_index=0, output_dir='../../subgrid_emu/subgrid_emu/data'):
    """
    Save training data for a specific statistic.
    
    Parameters
    ----------
    stat_name : str
        Name of the statistic (e.g., 'GSMF', 'fGas', 'CGD')
    params : np.array
        Parameter array (p_all)
    y_vals : np.array
        Target values
    y_ind : np.array
        Independent variable values
    z_index : int
        Redshift index
    output_dir : str
        Output directory path
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each component
    base_name = f"{stat_name}_z_index{z_index}"
    np.save(os.path.join(output_dir, f"{base_name}_params.npy"), params)
    np.save(os.path.join(output_dir, f"{base_name}_y_vals.npy"), y_vals)
    np.save(os.path.join(output_dir, f"{base_name}_y_ind.npy"), y_ind)
    
    print(f"Saved training data for {stat_name}:")
    print(f"  params shape: {params.shape}")
    print(f"  y_vals shape: {y_vals.shape}")
    print(f"  y_ind shape: {y_ind.shape}")


# Example usage - you need to run this with the actual data from the notebook
if __name__ == "__main__":
    print("This script needs to be run with actual training data from the notebook.")
    print("Copy the relevant data loading cells from final_compare_frontierE.ipynb")
    print("and call save_training_data() for each statistic.")
    print("\nExample:")
    print("  save_training_data('GSMF', params32, y_vals_gsmf, y_ind_gsmf)")
    print("  save_training_data('fGas', params32, y_vals_fgas, y_ind_fgas)")
    print("  save_training_data('CGD', params32, y_vals_cgd, y_ind_cgd)")
