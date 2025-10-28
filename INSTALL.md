# Installation Guide

## Quick Install

From the `subgrid_emu` directory:

```bash
pip install -e .
```

The `-e` flag installs in "editable" mode, which is useful for development.

## Dependencies

The package requires:
- Python >= 3.7
- numpy >= 1.18.0
- scipy >= 1.4.0
- sepia >= 1.0.0 (SEPIA package from LANL)

### Installing SEPIA

SEPIA (Simulation-Enabled Prediction, Inference, and Analysis) can be installed via:

```bash
pip install sepia
```

Or from source:
```bash
git clone https://github.com/lanl/SEPIA.git
cd SEPIA
pip install -e .
```

## Verification

After installation, verify the package works:

```python
import subgrid_emu
print(subgrid_emu.__version__)

# List available statistics
stats = subgrid_emu.list_available_statistics()
print(stats)

# Load a simple emulator
emu = subgrid_emu.load_emulator('GSMF')
print(emu)
```

## Package Structure

```
subgrid_emu/
├── README.md              # Main documentation
├── INSTALL.md            # This file
├── setup.py              # Installation script
├── examples/             # Example notebooks
│   └── basic_usage.ipynb
└── subgrid_emu/          # Main package
    ├── __init__.py       # Package initialization
    ├── emulator.py       # Core emulator class
    ├── data_utils.py     # Data utilities
    └── models/           # Pre-trained model files
        ├── GSMF_multivariate_model_z_index0.pkl
        ├── BHMSM_multivariate_model_z_index0.pkl
        ├── fGas_multivariate_model_z_index0.pkl
        ├── CGD_multivariate_model_z_index0.pkl
        ├── CGED_multivariate_model_z_index0.pkl
        ├── Pk_multivariate_model_z_index0.pkl
        ├── CSFR_multivariate_model_z_index0.pkl
        ├── CGD_2p_multivariate_model_z_index0.pkl
        ├── CGD_CC_2p_multivariate_model_z_index0.pkl
        └── fGas_2p_multivariate_model_z_index0.pkl
```

## Troubleshooting

### Import Error: No module named 'sepia'

Install SEPIA:
```bash
pip install sepia
```

### Model files not found

Make sure you installed with the `-e` flag or that `package_data` is properly configured in `setup.py`.

### Permission errors

Try installing in a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Development Installation

For development with additional tools:

```bash
pip install -e ".[dev]"
```

This installs extra packages for testing and development.

## Uninstallation

```bash
pip uninstall subgrid_emu
