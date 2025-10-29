"""
Setup script for the subgrid_emu package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
def get_version():
    init_file = os.path.join("subgrid_emu", "__init__.py")
    with open(init_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip("'\"")
    return "0.1.0"

setup(
    name="subgrid_emu",
    version=get_version(),
    author="Nesar Ramachandra",
    author_email="",  # Add email if desired
    description="Gaussian Process emulators for cosmological hydrodynamical simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nesar/subgrid_emu",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy==1.22.1",
        "scipy==1.10.1",
        "sepia @ git+https://github.com/lanl/SEPIA.git",
        "matplotlib==3.8.2",
        "pandas==1.5.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "matplotlib>=3.0",
        ],
        "plotting": [
            "matplotlib>=3.0",
        ],
    },
    package_data={
        "subgrid_emu": [
            "models/*.pkl",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="cosmology emulator gaussian-process hydrodynamics simulations",
    project_urls={
        "Bug Reports": "https://github.com/nesar/subgrid_emu/issues",
        "Source": "https://github.com/nesar/subgrid_emu",
    },
)
