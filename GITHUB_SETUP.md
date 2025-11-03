# GitHub CI/CD Setup Instructions

This document provides step-by-step instructions for setting up CI/CD for the `subgrid_emu` package on GitHub.

## Overview

The CI/CD pipeline has been configured to:
- Run automated tests on Python 3.9, 3.10, and 3.11
- Perform code quality checks (linting, formatting)
- Build the package and verify it can be installed
- Run integration tests
- Generate test coverage reports

## Prerequisites

Before proceeding, ensure you have:
1. A GitHub account
2. Git installed on your local machine
3. The subgrid_emu repository initialized locally

## Step 1: Push to GitHub

If you haven't already pushed the repository to GitHub, follow these steps:

### Option A: New Repository

1. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Repository name: `subgrid_emu`
   - Description: "Gaussian Process emulators for cosmological hydrodynamical simulations"
   - Choose Public or Private
   - Do NOT initialize with README (we already have one)
   - Click "Create repository"

2. Push your local repository:
   ```bash
   cd /home/nramachandra/Projects/Hydro_runs/subgrid_emu
   git init  # if not already initialized
   git add .
   git commit -m "Initial commit with CI/CD setup"
   git branch -M main
   git remote add origin https://github.com/nesar/subgrid_emu.git
   git push -u origin main
   ```

### Option B: Existing Repository

If the repository already exists on GitHub:

```bash
cd /home/nramachandra/Projects/Hydro_runs/subgrid_emu
git add .
git commit -m "Add CI/CD pipeline and test suite"
git push origin main
```

## Step 2: Verify GitHub Actions

1. Go to your repository on GitHub: `https://github.com/nesar/subgrid_emu`

2. Click on the "Actions" tab

3. You should see the CI/CD workflow running automatically

4. The workflow will run on:
   - Every push to `main`, `master`, or `develop` branches
   - Every pull request to these branches
   - Manual trigger (workflow_dispatch)

## Step 3: Add Status Badges (Optional)

Add CI/CD status badges to your README.md:

```markdown
# Emulator-suite for Cosmological summary statistics

[![CI/CD Pipeline](https://github.com/nesar/subgrid_emu/actions/workflows/ci.yml/badge.svg)](https://github.com/nesar/subgrid_emu/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/nesar/subgrid_emu/branch/main/graph/badge.svg)](https://codecov.io/gh/nesar/subgrid_emu)

[Rest of your README content...]
```

## Step 4: Set Up Codecov (Optional but Recommended)

To enable code coverage reporting:

1. Go to https://codecov.io/
2. Sign in with your GitHub account
3. Add the `subgrid_emu` repository
4. The workflow is already configured to upload coverage reports
5. No additional configuration needed!

## Step 5: Configure Branch Protection (Recommended)

To ensure code quality:

1. Go to your repository settings
2. Click "Branches" in the left sidebar
3. Click "Add rule" under "Branch protection rules"
4. Branch name pattern: `main`
5. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select status checks: `Test on Python 3.9`, `Test on Python 3.10`, `Test on Python 3.11`, `Build Package`
6. Click "Create"

## Step 6: Test the CI/CD Pipeline

### Manual Trigger

1. Go to the "Actions" tab
2. Click on "CI/CD Pipeline" in the left sidebar
3. Click "Run workflow" button
4. Select the branch (main)
5. Click "Run workflow"

### Test with a Pull Request

1. Create a new branch:
   ```bash
   git checkout -b test-ci
   ```

2. Make a small change (e.g., update README.md)

3. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin test-ci
   ```

4. Create a pull request on GitHub

5. Watch the CI/CD pipeline run automatically

## CI/CD Pipeline Details

### Jobs Overview

1. **Test** (Matrix: Python 3.9, 3.10, 3.11)
   - Installs dependencies
   - Runs pytest with coverage
   - Uploads coverage to Codecov

2. **Lint**
   - Checks code formatting with Black
   - Checks import sorting with isort
   - Runs flake8 for code quality

3. **Build**
   - Builds the package (wheel and source distribution)
   - Validates the package with twine
   - Uploads build artifacts

4. **Integration Test**
   - Downloads the built package
   - Installs from wheel
   - Tests basic functionality

### Running Tests Locally

Before pushing, you can run tests locally:

```bash
cd /home/nramachandra/Projects/Hydro_runs/subgrid_emu

# Install in development mode
pip install -e .

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=subgrid_emu --cov-report=term

# Run specific test file
pytest tests/test_emulator.py -v

# Run specific test
pytest tests/test_emulator.py::TestEmulatorLoading::test_load_5p_emulator -v
```

### Code Quality Checks Locally

```bash
# Install linting tools
pip install black isort flake8

# Check formatting
black --check subgrid_emu/ tests/

# Auto-format code
black subgrid_emu/ tests/

# Check import sorting
isort --check-only subgrid_emu/ tests/

# Auto-sort imports
isort subgrid_emu/ tests/

# Run flake8
flake8 subgrid_emu/ tests/ --max-line-length=100
```

## Troubleshooting

### Tests Fail on GitHub but Pass Locally

- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility
- Verify data files are included in the package

### Build Fails

- Check `setup.py` configuration
- Ensure `MANIFEST.in` includes all necessary files
- Verify package structure

### Coverage Upload Fails

- This is non-critical (set to `fail_ci_if_error: false`)
- Check Codecov integration if needed

## Maintenance

### Updating Dependencies

When updating dependencies:

1. Update `requirements.txt`
2. Update `setup.py` install_requires
3. Test locally
4. Push and verify CI/CD passes

### Adding New Tests

1. Create test files in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use pytest conventions
4. Run locally before pushing

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.com/)

## Support

For issues with the CI/CD setup, please open an issue on the GitHub repository.
