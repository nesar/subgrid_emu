# Pk Emulator Fix - Changelog

## Issue
The Pk (power spectrum) emulator was failing with a reshape error:
```
ValueError: cannot reshape array of size 6 into shape (6,2)
```

## Root Cause
The training data saved in the package had **443 k-points**, but the actual training in `gp_HACC_emu_pk.ipynb` used a masked dataset with **255 k-points**. This mismatch caused:
1. The deployment code to create 2 PCA components (with 443 points and exp_variance=0.95)
2. The saved model expected 1 PCA component (trained with 255 points and exp_variance=0.95)
3. This dimensional mismatch caused the reshape error during prediction

## Solution
Regenerated the Pk training data by applying the exact same mask used during training:

```python
mlim1, mlim2 = mass_conds('Pk')  # Returns (0.04908738521234052, 12.566370614359172)
mass_cond = np.where((k > mlim1) & (k < mlim2))
y_vals = pk_ratio[:, mass_cond][:, 0, :]
y_ind = k[mass_cond]
```

This reduced the data from 443 to 255 k-points, matching the training configuration.

## Files Modified

### 1. `subgrid_emu/subgrid_emu/model_metadata.py`
- Set Pk y_ind to `None` so it's loaded from the actual data files
- This ensures the k-grid matches exactly what was used in training (after masking)

### 2. `subgrid_emu/subgrid_emu/data/Pk_z_index0_y_ind.npy`
- Regenerated with 255 k-points (down from 443)

### 3. `subgrid_emu/subgrid_emu/data/Pk_z_index0_y_vals.npy`
- Regenerated with shape (64, 255) (down from (64, 443))

### 4. Created `subgrid_emu/scripts/regenerate_pk_data.py`
- Script to regenerate Pk data from source with correct masking
- Replicates the exact procedure from `gp_HACC_emu_pk.ipynb`

## Verification
All 6 statistics now work correctly:
- ✓ GSMF (shape=16)
- ✓ BHMSM (shape=7)
- ✓ fGas (shape=8)
- ✓ CGD (shape=19)
- ✓ **Pk (shape=255)** ← Fixed!
- ✓ CSFR (shape=655)

## Key Takeaway
The training data in the package must exactly match the data used during model training, including:
- Grid size (number of points)
- Grid values (after any masking)
- This ensures the PCA decomposition produces the same number of components

## Date
October 28, 2025
