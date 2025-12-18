# AMR Feature Correlation

A Python package for correlating microfluidics features with nanomotion and phenotypic features from antimicrobial resistance (AMR) experiments.

## Overview

This package provides tools to:
- Load and preprocess experimental data from multiple sources (microfluidics, nanomotion, phenotypic features)
- Compute correlation coefficients (Pearson and Spearman) between different feature sets
- Identify statistically significant correlations
- Visualize correlation results through heatmaps, scatter plots, and bar charts

## Features

- **Multi-format Support**: Load data from CSV, Excel, and TSV files
- **Flexible Correlation Methods**: Pearson and Spearman correlation with p-value computation
- **Data Preprocessing**: Handle missing values, normalize features, merge datasets
- **Rich Visualizations**: Create publication-ready heatmaps, scatter plots, and bar charts
- **Statistical Analysis**: Automatic identification of significant correlations
- **Modular Design**: Easy to extend and customize for specific analyses

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mar-ina-thal/AMR-feature-correlation.git
cd AMR-feature-correlation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Using the Command-Line Interface

Analyze correlations between microfluidics and nanomotion data:

```bash
python src/main.py \
    --microfluidics data/microfluidics.csv \
    --nanomotion data/nanomotion.csv \
    --method pearson \
    --output-dir results
```

Include phenotypic features:

```bash
python src/main.py \
    --microfluidics data/microfluidics.csv \
    --nanomotion data/nanomotion.csv \
    --phenotypic data/phenotypic.csv \
    --method spearman \
    --threshold 0.01 \
    --min-corr 0.6 \
    --output-dir results
```

### Using the Python API

```python
from amr_correlation import DataLoader, CorrelationAnalyzer, CorrelationVisualizer

# Load data
loader = DataLoader()
microfluidics = loader.load_microfluidics_data('microfluidics.csv', index_col='sample_id')
nanomotion = loader.load_nanomotion_data('nanomotion.csv', index_col='sample_id')

# Analyze correlations
analyzer = CorrelationAnalyzer()
results = analyzer.correlate_microfluidics_with_nanomotion(
    microfluidics, 
    nanomotion,
    method='pearson'
)

# Get significant correlations
significant = analyzer.get_significant_correlations(
    results['correlations'],
    results['pvalues'],
    threshold=0.05,
    min_corr=0.5
)

# Visualize results
visualizer = CorrelationVisualizer()
visualizer.plot_correlation_heatmap(
    results['correlations'],
    title='Microfluidics vs Nanomotion',
    save_path='correlation_heatmap.png'
)
```

## Example Usage

Run the example script to see the package in action:

```bash
python examples/example_usage.py
```

This will:
1. Generate synthetic example data
2. Perform correlation analysis
3. Create visualizations
4. Save results to `examples/output/`

## Data Format

Input files should be in CSV, Excel, or TSV format with:
- Each row representing a sample/observation
- First column containing sample IDs (optional)
- Subsequent columns containing numeric features

See [data/DATA_FORMAT.md](data/DATA_FORMAT.md) for detailed format specifications and examples.

## Package Structure

```
AMR-feature-correlation/
├── src/
│   ├── amr_correlation/
│   │   ├── __init__.py           # Package initialization
│   │   ├── data_loader.py        # Data loading and preprocessing
│   │   ├── correlation_analysis.py  # Correlation computation
│   │   └── visualization.py      # Visualization tools
│   └── main.py                   # Command-line interface
├── examples/
│   └── example_usage.py          # Example usage script
├── data/
│   └── DATA_FORMAT.md           # Data format documentation
├── tests/                        # Unit tests (to be added)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Command-Line Options

```
usage: main.py [-h] --microfluidics MICROFLUIDICS [--nanomotion NANOMOTION]
               [--phenotypic PHENOTYPIC] [--method {pearson,spearman}]
               [--output-dir OUTPUT_DIR] [--threshold THRESHOLD]
               [--min-corr MIN_CORR]

optional arguments:
  -h, --help            show this help message and exit
  --microfluidics MICROFLUIDICS
                        Path to microfluidics data file
  --nanomotion NANOMOTION
                        Path to nanomotion data file
  --phenotypic PHENOTYPIC
                        Path to phenotypic data file
  --method {pearson,spearman}
                        Correlation method (default: pearson)
  --output-dir OUTPUT_DIR
                        Directory to save results (default: results)
  --threshold THRESHOLD
                        P-value threshold for significance (default: 0.05)
  --min-corr MIN_CORR   Minimum absolute correlation (default: 0.5)
```

## Output Files

The analysis generates the following files in the output directory:

- `*_correlations.csv` - Correlation coefficient matrices
- `*_pvalues.csv` - P-value matrices
- `*_significant.csv` - Table of significant correlations
- `*_heatmap.png` - Correlation heatmap visualization
- `*_pvalues.png` - P-value heatmap with significance indicators
- `*_top.png` - Bar chart of top correlations (if significant correlations exist)

## Requirements

- Python >= 3.7
- pandas >= 1.5.0
- numpy >= 1.23.0
- scipy >= 1.9.0
- matplotlib >= 3.6.0
- seaborn >= 0.12.0
- openpyxl >= 3.0.0 (for Excel file support)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Citation

If you use this package in your research, please cite:

```
Filippidou, M.T. (2025). AMR Feature Correlation: A tool for correlating 
microfluidics features with nanomotion and phenotypic features.
GitHub repository: https://github.com/mar-ina-thal/AMR-feature-correlation
```

## Contact

Marina Thalassini Filippidou - [@mar-ina-thal](https://github.com/mar-ina-thal)

## Acknowledgments

This package was developed for analyzing correlations in antimicrobial resistance experiments, combining microfluidics, nanomotion, and phenotypic data.