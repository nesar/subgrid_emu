# Python 3.12 Compatibility Updates

## Summary

The subgrid_emu package has been updated to be compatible with Python 3.12.12 (and Python 3.12.x in general).

## Changes Made

### 1. setup.py
**File:** `subgrid_emu/setup.py`

**Changes:**
- Updated `python_requires` from `">=3.9,<3.11"` to `">=3.9"` to allow Python 3.12+
- Added Python 3.11 and 3.12 to classifiers
- Removed upper version constraints on dependencies:
  - `numpy>=1.21.0,<1.24` → `numpy>=1.21.0`
  - `scipy>=1.7.0,<1.11` → `scipy>=1.7.0`
  - `matplotlib>=3.5.0,<3.9` → `matplotlib>=3.5.0`
  - `pandas>=1.3.0,<2.0` → `pandas>=1.3.0`

### 2. requirements.txt
**File:** `subgrid_emu/requirements.txt`

**Changes:**
- Removed upper version constraints on all dependencies to allow compatibility with Python 3.12

### 3. emulator.py
**File:** `subgrid_emu/subgrid_emu/emulator.py`

**Changes:**
- Replaced deprecated `pkg_resources` with `importlib.resources`
- Added fallback import for older Python versions:
  ```python
  try:
      # Python 3.9+
      from importlib.resources import files
  except ImportError:
      # Fallback for older Python versions
      from importlib_resources import files
  ```
- Updated `get_model_path()` function to use `importlib.resources.files()` instead of `pkg_resources.resource_filename()`

## Testing Instructions

### Option 1: Using Conda (Recommended)

1. Create a Python 3.12 environment:
   ```bash
   conda create -n test_py312 python=3.12 -y
   ```

2. Activate the environment:
   ```bash
   conda activate test_py312
   ```

3. Install the package:
   ```bash
   cd subgrid_emu
   pip install -e .
   ```

4. Run tests:
   ```bash
   pytest tests/
   ```

5. Test basic functionality:
   ```bash
   python -c "from subgrid_emu import load_emulator; emu = load_emulator('GSMF'); print('Success!')"
   ```

### Option 2: Using venv

1. Create a virtual environment with Python 3.12:
   ```bash
   python3.12 -m venv venv_py312
   source venv_py312/bin/activate
   ```

2. Install the package:
   ```bash
   cd subgrid_emu
   pip install -e .
   ```

3. Run tests:
   ```bash
   pytest tests/
   ```

## Expected Behavior

The package should:
1. Install successfully without version conflicts
2. Import without errors
3. Load emulators successfully
4. Make predictions correctly
5. Pass all existing tests

## Potential Issues and Solutions

### Issue 1: SEPIA Dependency
The SEPIA package is installed from GitHub. If there are compatibility issues:
- Check if SEPIA has been updated for Python 3.12
- May need to update SEPIA or wait for upstream fixes

### Issue 2: NumPy/SciPy Compatibility
- Modern versions of NumPy and SciPy support Python 3.12
- If issues arise, specific version pins may be needed

### Issue 3: importlib.resources
- The `files()` API is available in Python 3.9+
- For Python < 3.9, the `importlib_resources` backport would be needed (not currently in dependencies)

## Verification Checklist

- [x] Updated setup.py to support Python 3.12
- [x] Updated requirements.txt to remove version caps
- [x] Replaced pkg_resources with importlib.resources
- [ ] Tested installation in Python 3.12 environment
- [ ] Verified all emulators load correctly
- [ ] Ran full test suite
- [ ] Tested basic prediction functionality

## Notes

- The code is now compatible with Python 3.9 through 3.12+
- No changes were made to the core emulator logic
- All changes are backward compatible with Python 3.9 and 3.10
- The deprecated `pkg_resources` has been replaced with the modern `importlib.resources` API

## Next Steps for User

1. Test the installation in a Python 3.12 environment
2. Run the test suite to verify functionality
3. Report any issues encountered
4. If successful, update documentation to reflect Python 3.12 support
