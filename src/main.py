"""
Main Script for AMR Feature Correlation Analysis
=================================================

This script demonstrates how to use the AMR correlation package to analyze
correlations between microfluidics, nanomotion, and phenotypic features.
"""

import argparse
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from amr_correlation import DataLoader, CorrelationAnalyzer, CorrelationVisualizer


def main():
    """Main function to run correlation analysis."""
    parser = argparse.ArgumentParser(
        description='Correlate microfluidics features with nanomotion and phenotypic features'
    )
    
    parser.add_argument(
        '--microfluidics',
        type=str,
        required=True,
        help='Path to microfluidics data file (CSV, Excel, or TSV)'
    )
    
    parser.add_argument(
        '--nanomotion',
        type=str,
        help='Path to nanomotion data file (CSV, Excel, or TSV)'
    )
    
    parser.add_argument(
        '--phenotypic',
        type=str,
        help='Path to phenotypic data file (CSV, Excel, or TSV)'
    )
    
    parser.add_argument(
        '--method',
        type=str,
        default='pearson',
        choices=['pearson', 'spearman'],
        help='Correlation method to use (default: pearson)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='results',
        help='Directory to save results (default: results)'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.05,
        help='P-value threshold for significance (default: 0.05)'
    )
    
    parser.add_argument(
        '--min-corr',
        type=float,
        default=0.5,
        help='Minimum absolute correlation coefficient (default: 0.5)'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Initialize components
    loader = DataLoader()
    analyzer = CorrelationAnalyzer()
    visualizer = CorrelationVisualizer()
    
    print("Loading data...")
    
    # Load microfluidics data
    microfluidics_data = loader.load_microfluidics_data(args.microfluidics)
    print(f"Loaded microfluidics data: {microfluidics_data.shape}")
    
    # Analyze correlations with nanomotion
    if args.nanomotion:
        print("\nAnalyzing microfluidics vs nanomotion correlations...")
        nanomotion_data = loader.load_nanomotion_data(args.nanomotion)
        print(f"Loaded nanomotion data: {nanomotion_data.shape}")
        
        results = analyzer.correlate_microfluidics_with_nanomotion(
            microfluidics_data,
            nanomotion_data,
            method=args.method
        )
        
        # Get significant correlations
        significant = analyzer.get_significant_correlations(
            results['correlations'],
            results['pvalues'],
            threshold=args.threshold,
            min_corr=args.min_corr
        )
        
        print(f"\nFound {len(significant)} significant correlations")
        
        # Save results
        results['correlations'].to_csv(
            output_dir / 'microfluidics_nanomotion_correlations.csv'
        )
        results['pvalues'].to_csv(
            output_dir / 'microfluidics_nanomotion_pvalues.csv'
        )
        significant.to_csv(
            output_dir / 'microfluidics_nanomotion_significant.csv',
            index=False
        )
        
        # Create visualizations
        visualizer.plot_correlation_heatmap(
            results['correlations'],
            title='Microfluidics vs Nanomotion Correlations',
            save_path=output_dir / 'microfluidics_nanomotion_heatmap.png'
        )
        
        visualizer.plot_pvalue_heatmap(
            results['pvalues'],
            title='Microfluidics vs Nanomotion P-values',
            threshold=args.threshold,
            save_path=output_dir / 'microfluidics_nanomotion_pvalues.png'
        )
        
        if len(significant) > 0:
            visualizer.plot_top_correlations(
                significant,
                title='Top Microfluidics-Nanomotion Correlations',
                save_path=output_dir / 'microfluidics_nanomotion_top.png'
            )
    
    # Analyze correlations with phenotypic features
    if args.phenotypic:
        print("\nAnalyzing microfluidics vs phenotypic correlations...")
        phenotypic_data = loader.load_phenotypic_data(args.phenotypic)
        print(f"Loaded phenotypic data: {phenotypic_data.shape}")
        
        results = analyzer.correlate_microfluidics_with_phenotypic(
            microfluidics_data,
            phenotypic_data,
            method=args.method
        )
        
        # Get significant correlations
        significant = analyzer.get_significant_correlations(
            results['correlations'],
            results['pvalues'],
            threshold=args.threshold,
            min_corr=args.min_corr
        )
        
        print(f"\nFound {len(significant)} significant correlations")
        
        # Save results
        results['correlations'].to_csv(
            output_dir / 'microfluidics_phenotypic_correlations.csv'
        )
        results['pvalues'].to_csv(
            output_dir / 'microfluidics_phenotypic_pvalues.csv'
        )
        significant.to_csv(
            output_dir / 'microfluidics_phenotypic_significant.csv',
            index=False
        )
        
        # Create visualizations
        visualizer.plot_correlation_heatmap(
            results['correlations'],
            title='Microfluidics vs Phenotypic Correlations',
            save_path=output_dir / 'microfluidics_phenotypic_heatmap.png'
        )
        
        visualizer.plot_pvalue_heatmap(
            results['pvalues'],
            title='Microfluidics vs Phenotypic P-values',
            threshold=args.threshold,
            save_path=output_dir / 'microfluidics_phenotypic_pvalues.png'
        )
        
        if len(significant) > 0:
            visualizer.plot_top_correlations(
                significant,
                title='Top Microfluidics-Phenotypic Correlations',
                save_path=output_dir / 'microfluidics_phenotypic_top.png'
            )
    
    print(f"\nResults saved to {output_dir}")
    print("Analysis complete!")


if __name__ == '__main__':
    main()
