"""Setup script for the AMR Feature Correlation package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="amr-feature-correlation",
    version="0.1.0",
    author="Marina Thalassini Filippidou",
    author_email="",
    description="A package for correlating microfluidics features with nanomotion and phenotypic features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mar-ina-thal/AMR-feature-correlation",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scipy>=1.9.0",
        "matplotlib>=3.6.0",
        "seaborn>=0.12.0",
        "openpyxl>=3.0.0",
    ],
    # Entry points commented out - use 'python src/main.py' to run
    # entry_points={
    #     "console_scripts": [
    #         "amr-correlate=amr_correlation.main:main",
    #     ],
    # },
)
