"""
Unit tests for the AMR Feature Correlation package.
"""

import unittest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from amr_correlation import DataLoader, CorrelationAnalyzer, CorrelationVisualizer


class TestDataLoader(unittest.TestCase):
    """Test the DataLoader class."""
    
    def setUp(self):
        """Set up test data."""
        self.loader = DataLoader()
        self.sample_ids = [f'Sample_{i}' for i in range(10)]
        
        # Create sample data
        self.test_data = pd.DataFrame({
            'feature1': np.random.randn(10),
            'feature2': np.random.randn(10),
            'feature3': np.random.randn(10),
        }, index=self.sample_ids)
    
    def test_preprocess_data_drop_missing(self):
        """Test preprocessing with dropping missing values."""
        data = self.test_data.copy()
        data.iloc[0, 0] = np.nan
        
        processed = self.loader.preprocess_data(data, handle_missing='drop')
        self.assertEqual(len(processed), 9)
    
    def test_preprocess_data_normalize(self):
        """Test data normalization."""
        processed = self.loader.preprocess_data(
            self.test_data, 
            normalize=True
        )
        
        # Check that values are between 0 and 1
        for col in processed.columns:
            self.assertGreaterEqual(processed[col].min(), 0)
            self.assertLessEqual(processed[col].max(), 1)
    
    def test_merge_datasets(self):
        """Test merging multiple datasets."""
        data1 = pd.DataFrame({'a': [1, 2, 3]}, index=['S1', 'S2', 'S3'])
        data2 = pd.DataFrame({'b': [4, 5, 6]}, index=['S1', 'S2', 'S3'])
        
        merged = self.loader.merge_datasets([data1, data2])
        
        self.assertEqual(merged.shape, (3, 2))
        self.assertIn('a', merged.columns)
        self.assertIn('b', merged.columns)


class TestCorrelationAnalyzer(unittest.TestCase):
    """Test the CorrelationAnalyzer class."""
    
    def setUp(self):
        """Set up test data."""
        self.analyzer = CorrelationAnalyzer()
        np.random.seed(42)
        
        self.sample_ids = [f'Sample_{i}' for i in range(50)]
        
        # Create correlated data
        self.data1 = pd.DataFrame({
            'feat1': np.random.randn(50),
            'feat2': np.random.randn(50),
        }, index=self.sample_ids)
        
        # Data2 correlated with data1
        self.data2 = pd.DataFrame({
            'feat3': self.data1['feat1'] * 0.8 + np.random.randn(50) * 0.2,
            'feat4': np.random.randn(50),
        }, index=self.sample_ids)
    
    def test_compute_pearson_correlation(self):
        """Test Pearson correlation computation."""
        corr_matrix = self.analyzer.compute_pearson_correlation(
            self.data1, self.data2
        )
        
        self.assertEqual(corr_matrix.shape, (2, 2))
        self.assertIsInstance(corr_matrix, pd.DataFrame)
        
        # Check that correlation values are between -1 and 1
        self.assertTrue((corr_matrix.abs() <= 1).all().all())
    
    def test_compute_spearman_correlation(self):
        """Test Spearman correlation computation."""
        corr_matrix = self.analyzer.compute_spearman_correlation(
            self.data1, self.data2
        )
        
        self.assertEqual(corr_matrix.shape, (2, 2))
        self.assertIsInstance(corr_matrix, pd.DataFrame)
        
        # Check that correlation values are between -1 and 1
        self.assertTrue((corr_matrix.abs() <= 1).all().all())
    
    def test_compute_pvalues(self):
        """Test p-value computation."""
        pval_matrix = self.analyzer.compute_pvalues(
            self.data1, self.data2, method='pearson'
        )
        
        self.assertEqual(pval_matrix.shape, (2, 2))
        self.assertIsInstance(pval_matrix, pd.DataFrame)
        
        # Check that p-values are between 0 and 1
        self.assertTrue((pval_matrix >= 0).all().all())
        self.assertTrue((pval_matrix <= 1).all().all())
    
    def test_get_significant_correlations(self):
        """Test filtering of significant correlations."""
        corr_matrix = self.analyzer.compute_pearson_correlation(
            self.data1, self.data2
        )
        pval_matrix = self.analyzer.compute_pvalues(
            self.data1, self.data2
        )
        
        significant = self.analyzer.get_significant_correlations(
            corr_matrix, pval_matrix, threshold=0.05, min_corr=0.3
        )
        
        self.assertIsInstance(significant, pd.DataFrame)
        
        # Check that all significant correlations meet criteria
        if len(significant) > 0:
            self.assertTrue((significant['P-value'] < 0.05).all())
            self.assertTrue((significant['Correlation'].abs() >= 0.3).all())


class TestCorrelationVisualizer(unittest.TestCase):
    """Test the CorrelationVisualizer class."""
    
    def setUp(self):
        """Set up test data."""
        self.visualizer = CorrelationVisualizer()
        
        # Create sample correlation matrix
        self.corr_matrix = pd.DataFrame(
            [[1.0, 0.8], [0.8, 1.0]],
            index=['feat1', 'feat2'],
            columns=['feat3', 'feat4']
        )
        
        self.pval_matrix = pd.DataFrame(
            [[0.0, 0.01], [0.01, 0.0]],
            index=['feat1', 'feat2'],
            columns=['feat3', 'feat4']
        )
    
    def test_plot_correlation_heatmap(self):
        """Test correlation heatmap creation."""
        fig = self.visualizer.plot_correlation_heatmap(self.corr_matrix)
        
        self.assertIsNotNone(fig)
        self.assertEqual(len(self.visualizer.figures), 1)
    
    def test_plot_pvalue_heatmap(self):
        """Test p-value heatmap creation."""
        fig = self.visualizer.plot_pvalue_heatmap(self.pval_matrix)
        
        self.assertIsNotNone(fig)
        self.assertGreater(len(self.visualizer.figures), 0)
    
    def test_close_all_figures(self):
        """Test closing all figures."""
        self.visualizer.plot_correlation_heatmap(self.corr_matrix)
        self.visualizer.close_all_figures()
        
        self.assertEqual(len(self.visualizer.figures), 0)


if __name__ == '__main__':
    unittest.main()
