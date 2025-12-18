# Tutorial: Getting Started with AMR Feature Correlation

This tutorial will guide you through using the AMR Feature Correlation package to analyze relationships between microfluidics, nanomotion, and phenotypic features.

## Quick Start

### Command Line Interface

```bash
python src/main.py \
    --microfluidics data/microfluidics.csv \
    --nanomotion data/nanomotion.csv \
    --output-dir results
```

## Python API

```python
from amr_correlation import DataLoader, CorrelationAnalyzer, CorrelationVisualizer

# Load data
loader = DataLoader()
microfluidics = loader.load_microfluidics_data('microfluidics.csv', index_col='sample_id')
nanomotion = loader.load_nanomotion_data('nanomotion.csv', index_col='sample_id')

# Analyze
analyzer = CorrelationAnalyzer()
results = analyzer.correlate_microfluidics_with_nanomotion(microfluidics, nanomotion)

# Get significant correlations
significant = analyzer.get_significant_correlations(
    results['correlations'],
    results['pvalues'],
    threshold=0.05,
    min_corr=0.5
)

# Visualize
visualizer = CorrelationVisualizer()
visualizer.plot_correlation_heatmap(results['correlations'], save_path='heatmap.png')
```

For more examples, see [example_usage.py](../examples/example_usage.py).
