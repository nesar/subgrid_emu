# Changelog: GSMF and BHMSM Scaling Fix

## Date: 2025-10-29

### Summary
Fixed scaling issues in GSMF and BHMSM emulator outputs to ensure correct physical units.

### Changes Made

#### 1. `subgrid_emu/emulator.py`
- **Modified**: `SubgridEmulator.predict()` method
- **Change**: Added automatic output transformations based on statistic type:
  - **GSMF**: Emulator outputs are now transformed to log10 space
    - Raw emulator output (linear) → `np.log10(pred_samps)`
    - This ensures GSMF values are in log10 space for plotting
  - **BHMSM**: Emulator outputs are now transformed from log10 to linear space
    - Raw emulator output (log10) → `10**pred_samps`
    - This ensures BHMSM values are in linear space for plotting
  - Other statistics (fGas, CGD, Pk, CSFR) remain unchanged

#### 2. `subgrid_emu/data_utils.py`
- **Modified**: `get_plot_info()` function for GSMF
- **Changes**:
  - Updated ylabel to reflect log10 transformation:
    - Old: `r"$\mathrm{d}n \, / \, \mathrm{d}\log_{10} M_{\mathrm{stars}}  \left[1 / (h^{-1}\mathrm{Mpc})^3  \right]$"`
    - New: `r"$\log_{10} \left[ \mathrm{d}n \, / \, \mathrm{d}\log_{10} M_{\mathrm{stars}} \right]  \left[1 / (h^{-1}\mathrm{Mpc})^3  \right]$"`
  - Changed yscale from 'log' to 'linear' (since values are already in log10 space)

### Technical Details

The transformations are applied to the prediction samples before calculating mean and quantiles:

```python
# GSMF: emulator outputs linear values, transform to log10
if self.stat_name == 'GSMF':
    pred_samps = np.log10(pred_samps)
# BHMSM: emulator outputs log10 values, transform to linear (10**)
elif self.stat_name == 'BHMSM':
    pred_samps = 10**pred_samps
```

This ensures that:
1. Users receive correctly scaled predictions without manual transformation
2. Uncertainty quantiles are calculated in the correct space
3. Plotting routines work correctly with the transformed values

### Impact

- **Breaking Change**: No - the API remains the same
- **User Impact**: Users will now receive correctly scaled predictions automatically
- **Backward Compatibility**: Existing code will work but will now get correctly scaled outputs
- **Notebooks**: The `basic_usage.ipynb` notebook will now show correct scaling without manual transformations

### Testing Recommendations

1. Verify GSMF predictions are in log10 space
2. Verify BHMSM predictions are in linear space (M_sun units)
3. Check that uncertainty bands are correctly scaled
4. Ensure other statistics (fGas, CGD, Pk, CSFR) remain unchanged

### Reference

This fix aligns the emulator outputs with the correct implementation shown in the reference plotting code, where:
- GSMF plots use: `np.log10(model_grid)` and `np.log10(model_var_grid)`
- BHMSM plots use: `10**model_grid` and `10**model_var_grid`
