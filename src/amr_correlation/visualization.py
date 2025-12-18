"""
Visualization Module
====================

Provides visualization tools for correlation results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Tuple, Union


class CorrelationVisualizer:
    """Visualize correlation results between experimental features."""
    
    def __init__(self, style: str = 'seaborn-v0_8'):
        """
        Initialize the CorrelationVisualizer.
        
        Parameters
        ----------
        style : str, default 'seaborn-v0_8'
            Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        self.figures = []
    
    def plot_correlation_heatmap(
        self,
        correlation_matrix: pd.DataFrame,
        title: str = "Correlation Heatmap",
        figsize: Tuple[int, int] = (10, 8),
        cmap: str = 'RdBu_r',
        annot: bool = True,
        fmt: str = '.2f',
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """
        Plot a heatmap of correlation coefficients.
        
        Parameters
        ----------
        correlation_matrix : pd.DataFrame
            Matrix of correlation coefficients
        title : str, default "Correlation Heatmap"
            Title for the plot
        figsize : tuple, default (10, 8)
            Figure size (width, height)
        cmap : str, default 'RdBu_r'
            Colormap to use
        annot : bool, default True
            Whether to annotate cells with values
        fmt : str, default '.2f'
            String formatting for annotations
        save_path : str or Path, optional
            Path to save the figure
            
        Returns
        -------
        matplotlib.figure.Figure
            The figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            correlation_matrix.astype(float),
            annot=annot,
            fmt=fmt,
            cmap=cmap,
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
            ax=ax
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel("Features (Dataset 2)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Features (Dataset 1)", fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        self.figures.append(fig)
        return fig
    
    def plot_pvalue_heatmap(
        self,
        pvalue_matrix: pd.DataFrame,
        title: str = "P-value Heatmap",
        figsize: Tuple[int, int] = (10, 8),
        threshold: float = 0.05,
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """
        Plot a heatmap of p-values with significance threshold.
        
        Parameters
        ----------
        pvalue_matrix : pd.DataFrame
            Matrix of p-values
        title : str, default "P-value Heatmap"
            Title for the plot
        figsize : tuple, default (10, 8)
            Figure size (width, height)
        threshold : float, default 0.05
            Significance threshold for highlighting
        save_path : str or Path, optional
            Path to save the figure
            
        Returns
        -------
        matplotlib.figure.Figure
            The figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create significance mask
        significance_mask = pvalue_matrix < threshold
        
        sns.heatmap(
            pvalue_matrix.astype(float),
            annot=True,
            fmt='.3f',
            cmap='YlOrRd_r',
            vmin=0,
            vmax=0.1,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8, "label": "P-value"},
            ax=ax
        )
        
        # Highlight significant cells
        for i in range(len(pvalue_matrix.index)):
            for j in range(len(pvalue_matrix.columns)):
                if significance_mask.iloc[i, j]:
                    ax.add_patch(plt.Rectangle(
                        (j, i), 1, 1,
                        fill=False,
                        edgecolor='green',
                        lw=3
                    ))
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel("Features (Dataset 2)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Features (Dataset 1)", fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        self.figures.append(fig)
        return fig
    
    def plot_scatter_with_correlation(
        self,
        data1: pd.DataFrame,
        data2: pd.DataFrame,
        feature1: str,
        feature2: str,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (8, 6),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """
        Plot scatter plot with correlation line for two features.
        
        Parameters
        ----------
        data1 : pd.DataFrame
            First dataset
        data2 : pd.DataFrame
            Second dataset
        feature1 : str
            Feature name from data1
        feature2 : str
            Feature name from data2
        title : str, optional
            Title for the plot
        figsize : tuple, default (8, 6)
            Figure size (width, height)
        save_path : str or Path, optional
            Path to save the figure
            
        Returns
        -------
        matplotlib.figure.Figure
            The figure object
        """
        # Align data on common index
        common_idx = data1.index.intersection(data2.index)
        x = data1.loc[common_idx, feature1]
        y = data2.loc[common_idx, feature2]
        
        # Remove NaN values
        mask = ~(x.isna() | y.isna())
        x = x[mask]
        y = y[mask]
        
        # Compute correlation
        from scipy import stats
        corr, pval = stats.pearsonr(x, y)
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.scatter(x, y, alpha=0.6, s=50)
        
        # Add regression line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        x_line = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
        
        # Add correlation info
        ax.text(
            0.05, 0.95,
            f'r = {corr:.3f}\np = {pval:.3e}\nn = {len(x)}',
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=10
        )
        
        if title is None:
            title = f'{feature1} vs {feature2}'
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(feature1, fontsize=12)
        ax.set_ylabel(feature2, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        self.figures.append(fig)
        return fig
    
    def plot_top_correlations(
        self,
        significant_correlations: pd.DataFrame,
        top_n: int = 10,
        title: str = "Top Correlations",
        figsize: Tuple[int, int] = (10, 6),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """
        Plot bar chart of top correlations.
        
        Parameters
        ----------
        significant_correlations : pd.DataFrame
            DataFrame with significant correlations
        top_n : int, default 10
            Number of top correlations to show
        title : str, default "Top Correlations"
            Title for the plot
        figsize : tuple, default (10, 6)
            Figure size (width, height)
        save_path : str or Path, optional
            Path to save the figure
            
        Returns
        -------
        matplotlib.figure.Figure
            The figure object
        """
        # Sort by absolute correlation value
        df = significant_correlations.copy()
        df['abs_corr'] = df['Correlation'].abs()
        df = df.sort_values('abs_corr', ascending=False).head(top_n)
        
        # Create labels
        df['label'] = df['Feature1'] + ' - ' + df['Feature2']
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = ['red' if x < 0 else 'blue' for x in df['Correlation']]
        ax.barh(df['label'], df['Correlation'], color=colors, alpha=0.7)
        
        ax.set_xlabel('Correlation Coefficient', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        self.figures.append(fig)
        return fig
    
    def close_all_figures(self):
        """Close all figures created by the visualizer."""
        for fig in self.figures:
            plt.close(fig)
        self.figures = []
