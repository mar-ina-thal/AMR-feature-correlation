"""
Example Usage Script
====================

This script demonstrates how to use the AMR correlation package with example data.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from amr_correlation import DataLoader, CorrelationAnalyzer, CorrelationVisualizer


def generate_example_data():
    """Generate example datasets for demonstration."""
    np.random.seed(42)
    n_samples = 50
    
    # Generate sample IDs
    sample_ids = [f'Sample_{i:03d}' for i in range(n_samples)]
    
    # Microfluidics features
    microfluidics_data = pd.DataFrame({
        'flow_rate': np.random.normal(100, 15, n_samples),
        'pressure': np.random.normal(50, 8, n_samples),
        'velocity': np.random.normal(20, 3, n_samples),
        'viscosity': np.random.normal(1.2, 0.2, n_samples),
    }, index=sample_ids)
    
    # Nanomotion features (correlated with microfluidics)
    nanomotion_data = pd.DataFrame({
        'amplitude': microfluidics_data['flow_rate'] * 0.5 + np.random.normal(0, 5, n_samples),
        'frequency': microfluidics_data['pressure'] * 0.3 + np.random.normal(0, 3, n_samples),
        'displacement': microfluidics_data['velocity'] * 0.8 + np.random.normal(0, 2, n_samples),
    }, index=sample_ids)
    
    # Phenotypic features (some correlation with microfluidics)
    phenotypic_data = pd.DataFrame({
        'growth_rate': microfluidics_data['flow_rate'] * 0.01 + np.random.normal(0, 0.5, n_samples),
        'biofilm_formation': np.random.choice([0, 1, 2], n_samples),
        'motility': microfluidics_data['velocity'] * 0.05 + np.random.normal(0, 0.3, n_samples),
        'antibiotic_resistance': np.random.choice([0, 1], n_samples),
    }, index=sample_ids)
    
    return microfluidics_data, nanomotion_data, phenotypic_data


def main():
    """Run example analysis."""
    print("=" * 60)
    print("AMR Feature Correlation - Example Usage")
    print("=" * 60)
    
    # Generate example data
    print("\n1. Generating example data...")
    microfluidics_data, nanomotion_data, phenotypic_data = generate_example_data()
    
    print(f"   Microfluidics data shape: {microfluidics_data.shape}")
    print(f"   Nanomotion data shape: {nanomotion_data.shape}")
    print(f"   Phenotypic data shape: {phenotypic_data.shape}")
    
    # Initialize components
    print("\n2. Initializing analyzer and visualizer...")
    analyzer = CorrelationAnalyzer()
    visualizer = CorrelationVisualizer()
    
    # Analyze microfluidics vs nanomotion correlations
    print("\n3. Analyzing microfluidics vs nanomotion correlations...")
    results_nano = analyzer.correlate_microfluidics_with_nanomotion(
        microfluidics_data,
        nanomotion_data,
        method='pearson'
    )
    
    print("\n   Correlation Matrix:")
    print(results_nano['correlations'])
    
    # Get significant correlations
    significant_nano = analyzer.get_significant_correlations(
        results_nano['correlations'],
        results_nano['pvalues'],
        threshold=0.05,
        min_corr=0.5
    )
    
    print(f"\n   Found {len(significant_nano)} significant correlations")
    if len(significant_nano) > 0:
        print("\n   Top significant correlations:")
        print(significant_nano.head())
    
    # Analyze microfluidics vs phenotypic correlations
    print("\n4. Analyzing microfluidics vs phenotypic correlations...")
    results_pheno = analyzer.correlate_microfluidics_with_phenotypic(
        microfluidics_data,
        phenotypic_data,
        method='pearson'
    )
    
    print("\n   Correlation Matrix:")
    print(results_pheno['correlations'])
    
    significant_pheno = analyzer.get_significant_correlations(
        results_pheno['correlations'],
        results_pheno['pvalues'],
        threshold=0.05,
        min_corr=0.3
    )
    
    print(f"\n   Found {len(significant_pheno)} significant correlations")
    if len(significant_pheno) > 0:
        print("\n   Top significant correlations:")
        print(significant_pheno.head())
    
    # Create visualizations
    print("\n5. Creating visualizations...")
    
    output_dir = Path(__file__).parent.parent / 'examples' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Microfluidics vs Nanomotion visualizations
    visualizer.plot_correlation_heatmap(
        results_nano['correlations'],
        title='Microfluidics vs Nanomotion Correlations',
        save_path=output_dir / 'example_nano_heatmap.png'
    )
    print(f"   Saved: {output_dir / 'example_nano_heatmap.png'}")
    
    visualizer.plot_pvalue_heatmap(
        results_nano['pvalues'],
        title='Microfluidics vs Nanomotion P-values',
        save_path=output_dir / 'example_nano_pvalues.png'
    )
    print(f"   Saved: {output_dir / 'example_nano_pvalues.png'}")
    
    # Microfluidics vs Phenotypic visualizations
    visualizer.plot_correlation_heatmap(
        results_pheno['correlations'],
        title='Microfluidics vs Phenotypic Correlations',
        save_path=output_dir / 'example_pheno_heatmap.png'
    )
    print(f"   Saved: {output_dir / 'example_pheno_heatmap.png'}")
    
    # Scatter plot example
    if len(significant_nano) > 0:
        top_corr = significant_nano.iloc[0]
        visualizer.plot_scatter_with_correlation(
            microfluidics_data,
            nanomotion_data,
            top_corr['Feature1'],
            top_corr['Feature2'],
            save_path=output_dir / 'example_scatter.png'
        )
        print(f"   Saved: {output_dir / 'example_scatter.png'}")
    
    print("\n" + "=" * 60)
    print("Example analysis complete!")
    print(f"Results saved to: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
