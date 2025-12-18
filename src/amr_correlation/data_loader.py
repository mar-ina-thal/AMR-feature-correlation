"""
Data Loading Module
===================

Handles loading and preprocessing of microfluidics, nanomotion, and 
phenotypic feature data from various file formats.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Union, List


class DataLoader:
    """Load and preprocess experimental data from multiple sources."""
    
    def __init__(self):
        """Initialize the DataLoader."""
        self.microfluidics_data = None
        self.nanomotion_data = None
        self.phenotypic_data = None
        
    def load_microfluidics_data(
        self, 
        filepath: Union[str, Path],
        index_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load microfluidics feature data.
        
        Parameters
        ----------
        filepath : str or Path
            Path to the microfluidics data file (CSV, Excel, or TSV)
        index_col : str, optional
            Column to use as index (e.g., sample ID)
            
        Returns
        -------
        pd.DataFrame
            Loaded microfluidics data
        """
        filepath = Path(filepath)
        
        if filepath.suffix == '.csv':
            data = pd.read_csv(filepath, index_col=index_col)
        elif filepath.suffix in ['.xlsx', '.xls']:
            data = pd.read_excel(filepath, index_col=index_col)
        elif filepath.suffix == '.tsv':
            data = pd.read_csv(filepath, sep='\t', index_col=index_col)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        self.microfluidics_data = data
        return data
    
    def load_nanomotion_data(
        self, 
        filepath: Union[str, Path],
        index_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load nanomotion feature data.
        
        Parameters
        ----------
        filepath : str or Path
            Path to the nanomotion data file (CSV, Excel, or TSV)
        index_col : str, optional
            Column to use as index (e.g., sample ID)
            
        Returns
        -------
        pd.DataFrame
            Loaded nanomotion data
        """
        filepath = Path(filepath)
        
        if filepath.suffix == '.csv':
            data = pd.read_csv(filepath, index_col=index_col)
        elif filepath.suffix in ['.xlsx', '.xls']:
            data = pd.read_excel(filepath, index_col=index_col)
        elif filepath.suffix == '.tsv':
            data = pd.read_csv(filepath, sep='\t', index_col=index_col)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        self.nanomotion_data = data
        return data
    
    def load_phenotypic_data(
        self, 
        filepath: Union[str, Path],
        index_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load phenotypic feature data.
        
        Parameters
        ----------
        filepath : str or Path
            Path to the phenotypic data file (CSV, Excel, or TSV)
        index_col : str, optional
            Column to use as index (e.g., sample ID)
            
        Returns
        -------
        pd.DataFrame
            Loaded phenotypic data
        """
        filepath = Path(filepath)
        
        if filepath.suffix == '.csv':
            data = pd.read_csv(filepath, index_col=index_col)
        elif filepath.suffix in ['.xlsx', '.xls']:
            data = pd.read_excel(filepath, index_col=index_col)
        elif filepath.suffix == '.tsv':
            data = pd.read_csv(filepath, sep='\t', index_col=index_col)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        self.phenotypic_data = data
        return data
    
    def merge_datasets(
        self,
        datasets: List[pd.DataFrame],
        on: Optional[str] = None,
        how: str = 'inner'
    ) -> pd.DataFrame:
        """
        Merge multiple datasets on common index or column.
        
        Parameters
        ----------
        datasets : list of pd.DataFrame
            List of dataframes to merge
        on : str, optional
            Column name to merge on. If None, uses index.
        how : str, default 'inner'
            Type of merge ('inner', 'outer', 'left', 'right')
            
        Returns
        -------
        pd.DataFrame
            Merged dataset
        """
        if len(datasets) < 2:
            raise ValueError("Need at least 2 datasets to merge")
        
        result = datasets[0]
        for df in datasets[1:]:
            if on is None:
                result = result.merge(df, left_index=True, right_index=True, how=how)
            else:
                result = result.merge(df, on=on, how=how)
        
        return result
    
    def preprocess_data(
        self,
        data: pd.DataFrame,
        handle_missing: str = 'drop',
        normalize: bool = False
    ) -> pd.DataFrame:
        """
        Preprocess data by handling missing values and normalizing.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input data to preprocess
        handle_missing : str, default 'drop'
            How to handle missing values ('drop', 'mean', 'median', 'zero')
        normalize : bool, default False
            Whether to normalize features to [0, 1] range
            
        Returns
        -------
        pd.DataFrame
            Preprocessed data
        """
        data = data.copy()
        
        # Handle missing values
        if handle_missing == 'drop':
            data = data.dropna()
        elif handle_missing == 'mean':
            data = data.fillna(data.mean())
        elif handle_missing == 'median':
            data = data.fillna(data.median())
        elif handle_missing == 'zero':
            data = data.fillna(0)
        
        # Normalize if requested
        if normalize:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            data[numeric_cols] = (data[numeric_cols] - data[numeric_cols].min()) / \
                                  (data[numeric_cols].max() - data[numeric_cols].min())
        
        return data
