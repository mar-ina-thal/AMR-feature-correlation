"""
AMR Feature Correlation Package
================================

A package for correlating microfluidics features with nanomotion and 
phenotypic features from antimicrobial resistance (AMR) experiments.
"""

__version__ = "0.1.0"
__author__ = "Marina Thalassini Filippidou"

from .data_loader import DataLoader
from .correlation_analysis import CorrelationAnalyzer
from .visualization import CorrelationVisualizer

__all__ = [
    "DataLoader",
    "CorrelationAnalyzer",
    "CorrelationVisualizer",
]
