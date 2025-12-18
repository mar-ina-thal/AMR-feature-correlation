# Data Format Documentation

This document describes the expected format for input data files.

## Supported File Formats

The AMR correlation package supports the following file formats:
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- TSV (`.tsv`)

## Data Structure

All input files should follow these general guidelines:

### 1. Sample Identification
- Each row should represent a single sample/observation
- The first column should contain unique sample IDs (optional but recommended)
- Sample IDs should match across all input files for proper correlation

### 2. Feature Columns
- Each subsequent column should represent a feature/measurement
- Column headers should be descriptive and unique
- Numeric features should be properly formatted (no special characters except decimal points)

## Microfluidics Data

Microfluidics data typically includes measurements from microfluidic experiments:

**Example columns:**
- `sample_id` - Unique identifier for each sample
- `flow_rate` - Flow rate measurement (µL/min)
- `pressure` - Pressure measurement (kPa)
- `velocity` - Fluid velocity (mm/s)
- `viscosity` - Viscosity measurement (mPa·s)
- `temperature` - Temperature (°C)
- `channel_width` - Channel width (µm)
- `channel_height` - Channel height (µm)

**Example CSV format:**
```csv
sample_id,flow_rate,pressure,velocity,viscosity,temperature
Sample_001,95.2,48.3,19.5,1.18,25.0
Sample_002,102.1,51.7,20.8,1.22,25.1
Sample_003,98.5,49.1,19.8,1.20,24.9
```

## Nanomotion Data

Nanomotion data includes measurements of bacterial nanomotion:

**Example columns:**
- `sample_id` - Unique identifier (must match microfluidics data)
- `amplitude` - Nanomotion amplitude (nm)
- `frequency` - Oscillation frequency (Hz)
- `displacement` - Total displacement (nm)
- `response_time` - Time to detect motion (s)
- `peak_velocity` - Peak velocity of nanomotion (nm/s)

**Example CSV format:**
```csv
sample_id,amplitude,frequency,displacement,response_time
Sample_001,45.2,15.3,38.1,120.5
Sample_002,52.1,16.8,42.3,115.2
Sample_003,48.7,15.9,39.5,118.0
```

## Phenotypic Data

Phenotypic data includes observable characteristics and experimental results:

**Example columns:**
- `sample_id` - Unique identifier (must match other datasets)
- `growth_rate` - Growth rate (1/h)
- `biofilm_formation` - Biofilm formation score (0-3)
- `motility` - Motility measurement (mm)
- `antibiotic_resistance` - Resistance classification (0=sensitive, 1=resistant)
- `colony_morphology` - Colony appearance (categorical)
- `pigmentation` - Pigmentation level (0-3)

**Example CSV format:**
```csv
sample_id,growth_rate,biofilm_formation,motility,antibiotic_resistance
Sample_001,0.95,2,1.2,0
Sample_002,1.02,1,1.5,1
Sample_003,0.98,2,1.3,0
```

## Data Quality Requirements

### Missing Values
- Missing values can be handled by the package (drop, impute with mean/median, or zero)
- Minimize missing values for better correlation results
- Use `NaN`, `NA`, or leave cells empty to indicate missing values

### Data Types
- Numeric features should be float or integer values
- Categorical features should be encoded as integers or strings
- Boolean features should be 0/1 or True/False

### Sample Matching
- Sample IDs must match across datasets for correlation analysis
- The package will automatically align datasets on common sample IDs
- Only common samples will be used in correlation calculations

## Example Workflow

1. Prepare your data files in one of the supported formats
2. Ensure sample IDs are consistent across files
3. Check for missing values and outliers
4. Use the `DataLoader` class to load your data:

```python
from amr_correlation import DataLoader

loader = DataLoader()
microfluidics = loader.load_microfluidics_data('microfluidics.csv', index_col='sample_id')
nanomotion = loader.load_nanomotion_data('nanomotion.csv', index_col='sample_id')
phenotypic = loader.load_phenotypic_data('phenotypic.csv', index_col='sample_id')
```

5. Preprocess if needed:

```python
microfluidics = loader.preprocess_data(microfluidics, handle_missing='mean', normalize=True)
```

6. Run correlation analysis:

```python
from amr_correlation import CorrelationAnalyzer

analyzer = CorrelationAnalyzer()
results = analyzer.correlate_microfluidics_with_nanomotion(
    microfluidics, 
    nanomotion,
    method='pearson'
)
```
