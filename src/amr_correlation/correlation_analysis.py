"""
Correlation Analysis Module
============================

Performs correlation analysis between microfluidics features and 
nanomotion/phenotypic features.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple, Union


class CorrelationAnalyzer:
    """Analyze correlations between different experimental features."""
    
    def __init__(self):
        """Initialize the CorrelationAnalyzer."""
        self.correlation_results = {}
        
    def compute_pearson_correlation(
        self,
        data1: pd.DataFrame,
        data2: pd.DataFrame,
        features1: Optional[List[str]] = None,
        features2: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Compute Pearson correlation coefficients between features.
        
        Parameters
        ----------
        data1 : pd.DataFrame
            First dataset (e.g., microfluidics features)
        data2 : pd.DataFrame
            Second dataset (e.g., nanomotion or phenotypic features)
        features1 : list of str, optional
            Features from data1 to correlate. If None, uses all numeric columns.
        features2 : list of str, optional
            Features from data2 to correlate. If None, uses all numeric columns.
            
        Returns
        -------
        pd.DataFrame
            Correlation matrix with coefficients
        """
        if features1 is None:
            features1 = data1.select_dtypes(include=[np.number]).columns.tolist()
        if features2 is None:
            features2 = data2.select_dtypes(include=[np.number]).columns.tolist()
        
        # Align datasets on common index
        common_idx = data1.index.intersection(data2.index)
        data1_aligned = data1.loc[common_idx, features1]
        data2_aligned = data2.loc[common_idx, features2]
        
        # Compute correlation matrix
        correlation_matrix = pd.DataFrame(
            index=features1,
            columns=features2,
            dtype=float
        )
        
        for feat1 in features1:
            for feat2 in features2:
                corr, _ = stats.pearsonr(
                    data1_aligned[feat1].dropna(),
                    data2_aligned[feat2].dropna()
                )
                correlation_matrix.loc[feat1, feat2] = corr
        
        self.correlation_results['pearson'] = correlation_matrix
        return correlation_matrix
    
    def compute_spearman_correlation(
        self,
        data1: pd.DataFrame,
        data2: pd.DataFrame,
        features1: Optional[List[str]] = None,
        features2: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Compute Spearman rank correlation coefficients between features.
        
        Parameters
        ----------
        data1 : pd.DataFrame
            First dataset (e.g., microfluidics features)
        data2 : pd.DataFrame
            Second dataset (e.g., nanomotion or phenotypic features)
        features1 : list of str, optional
            Features from data1 to correlate. If None, uses all numeric columns.
        features2 : list of str, optional
            Features from data2 to correlate. If None, uses all numeric columns.
            
        Returns
        -------
        pd.DataFrame
            Correlation matrix with coefficients
        """
        if features1 is None:
            features1 = data1.select_dtypes(include=[np.number]).columns.tolist()
        if features2 is None:
            features2 = data2.select_dtypes(include=[np.number]).columns.tolist()
        
        # Align datasets on common index
        common_idx = data1.index.intersection(data2.index)
        data1_aligned = data1.loc[common_idx, features1]
        data2_aligned = data2.loc[common_idx, features2]
        
        # Compute correlation matrix
        correlation_matrix = pd.DataFrame(
            index=features1,
            columns=features2,
            dtype=float
        )
        
        for feat1 in features1:
            for feat2 in features2:
                corr, _ = stats.spearmanr(
                    data1_aligned[feat1].dropna(),
                    data2_aligned[feat2].dropna()
                )
                correlation_matrix.loc[feat1, feat2] = corr
        
        self.correlation_results['spearman'] = correlation_matrix
        return correlation_matrix
    
    def compute_pvalues(
        self,
        data1: pd.DataFrame,
        data2: pd.DataFrame,
        features1: Optional[List[str]] = None,
        features2: Optional[List[str]] = None,
        method: str = 'pearson'
    ) -> pd.DataFrame:
        """
        Compute p-values for correlation coefficients.
        
        Parameters
        ----------
        data1 : pd.DataFrame
            First dataset
        data2 : pd.DataFrame
            Second dataset
        features1 : list of str, optional
            Features from data1 to correlate
        features2 : list of str, optional
            Features from data2 to correlate
        method : str, default 'pearson'
            Correlation method ('pearson' or 'spearman')
            
        Returns
        -------
        pd.DataFrame
            Matrix of p-values
        """
        if features1 is None:
            features1 = data1.select_dtypes(include=[np.number]).columns.tolist()
        if features2 is None:
            features2 = data2.select_dtypes(include=[np.number]).columns.tolist()
        
        # Align datasets on common index
        common_idx = data1.index.intersection(data2.index)
        data1_aligned = data1.loc[common_idx, features1]
        data2_aligned = data2.loc[common_idx, features2]
        
        # Compute p-values
        pvalue_matrix = pd.DataFrame(
            index=features1,
            columns=features2,
            dtype=float
        )
        
        corr_func = stats.pearsonr if method == 'pearson' else stats.spearmanr
        
        for feat1 in features1:
            for feat2 in features2:
                _, pval = corr_func(
                    data1_aligned[feat1].dropna(),
                    data2_aligned[feat2].dropna()
                )
                pvalue_matrix.loc[feat1, feat2] = pval
        
        self.correlation_results[f'{method}_pvalues'] = pvalue_matrix
        return pvalue_matrix
    
    def get_significant_correlations(
        self,
        correlation_matrix: pd.DataFrame,
        pvalue_matrix: pd.DataFrame,
        threshold: float = 0.05,
        min_corr: float = 0.5
    ) -> pd.DataFrame:
        """
        Filter significant correlations based on p-value and correlation strength.
        
        Parameters
        ----------
        correlation_matrix : pd.DataFrame
            Matrix of correlation coefficients
        pvalue_matrix : pd.DataFrame
            Matrix of p-values
        threshold : float, default 0.05
            P-value threshold for significance
        min_corr : float, default 0.5
            Minimum absolute correlation coefficient
            
        Returns
        -------
        pd.DataFrame
            DataFrame with significant correlations
        """
        significant = []
        
        for feat1 in correlation_matrix.index:
            for feat2 in correlation_matrix.columns:
                corr = correlation_matrix.loc[feat1, feat2]
                pval = pvalue_matrix.loc[feat1, feat2]
                
                if pval < threshold and abs(corr) >= min_corr:
                    significant.append({
                        'Feature1': feat1,
                        'Feature2': feat2,
                        'Correlation': corr,
                        'P-value': pval
                    })
        
        return pd.DataFrame(significant)
    
    def correlate_microfluidics_with_nanomotion(
        self,
        microfluidics_data: pd.DataFrame,
        nanomotion_data: pd.DataFrame,
        method: str = 'pearson'
    ) -> Dict[str, pd.DataFrame]:
        """
        Correlate microfluidics features with nanomotion features.
        
        Parameters
        ----------
        microfluidics_data : pd.DataFrame
            Microfluidics feature data
        nanomotion_data : pd.DataFrame
            Nanomotion feature data
        method : str, default 'pearson'
            Correlation method ('pearson' or 'spearman')
            
        Returns
        -------
        dict
            Dictionary containing correlation matrix and p-values
        """
        if method == 'pearson':
            corr_matrix = self.compute_pearson_correlation(
                microfluidics_data, nanomotion_data
            )
        else:
            corr_matrix = self.compute_spearman_correlation(
                microfluidics_data, nanomotion_data
            )
        
        pval_matrix = self.compute_pvalues(
            microfluidics_data, nanomotion_data, method=method
        )
        
        return {
            'correlations': corr_matrix,
            'pvalues': pval_matrix
        }
    
    def correlate_microfluidics_with_phenotypic(
        self,
        microfluidics_data: pd.DataFrame,
        phenotypic_data: pd.DataFrame,
        method: str = 'pearson'
    ) -> Dict[str, pd.DataFrame]:
        """
        Correlate microfluidics features with phenotypic features.
        
        Parameters
        ----------
        microfluidics_data : pd.DataFrame
            Microfluidics feature data
        phenotypic_data : pd.DataFrame
            Phenotypic feature data
        method : str, default 'pearson'
            Correlation method ('pearson' or 'spearman')
            
        Returns
        -------
        dict
            Dictionary containing correlation matrix and p-values
        """
        if method == 'pearson':
            corr_matrix = self.compute_pearson_correlation(
                microfluidics_data, phenotypic_data
            )
        else:
            corr_matrix = self.compute_spearman_correlation(
                microfluidics_data, phenotypic_data
            )
        
        pval_matrix = self.compute_pvalues(
            microfluidics_data, phenotypic_data, method=method
        )
        
        return {
            'correlations': corr_matrix,
            'pvalues': pval_matrix
        }
