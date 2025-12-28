# Quick Start Guide - AST SpaceMobile Library

## Installation

```bash
cd /home/amouroug/ast_space_mobile_data
pip install -e .
```

## Verify Installation

```bash
python -c "import ast_spacemobile; print('✓ Installed version:', ast_spacemobile.__version__)"
```

## Usage

### 1. Generate Trajectory Report (CLI)

```bash
# Default date range (Dec 7-12, 2025)
python -m ast_spacemobile.cli.trajectory

# Custom date range
python -m ast_spacemobile.cli.trajectory --start 2025-12-01 --end 2025-12-15

# Single day
python -m ast_spacemobile.cli.trajectory --start 2025-12-10 --end 2025-12-10
```

**Output:**
- `ast_satellite_data_<dates>.json` - Complete data
- `ast_<satellite>_<dates>.csv` - Per-satellite CSVs
- `AST_SpaceMobile_Satellite_Report_<dates>.md` - Markdown report

### 2. Generate Pass Analysis Report (CLI)

```bash
# Auto-detect latest data file
python -m ast_spacemobile.cli.passes

# Specify data file
python -m ast_spacemobile.cli.passes --data ast_satellite_data_dec7-12.json

# Custom output directory
python -m ast_spacemobile.cli.passes --output-dir my_graphs
```

**Output:**
- `AST_SpaceMobile_Detailed_Pass_Report.md` - Detailed report
- `pass_graphs/*.png` - Signal strength graphs

### 3. Run Complete Pipeline (CLI)

```bash
# Full pipeline
python -m ast_spacemobile.cli.pipeline

# Custom dates
python -m ast_spacemobile.cli.pipeline --start 2025-12-01 --end 2025-12-15

# Skip steps
python -m ast_spacemobile.cli.pipeline --skip-data     # Use existing data
python -m ast_spacemobile.cli.pipeline --skip-passes   # Use existing report
python -m ast_spacemobile.cli.pipeline --skip-pdf      # Skip PDF
```

### 4. Python API

#### Basic Usage

```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report, generate_pass_report

# Generate trajectory report
data, report_file = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12)
)

print(f"Report saved to: {report_file}")
print(f"Tracked {len(data)} satellites")

# Generate pass analysis
pass_report = generate_pass_report()
print(f"Pass report saved to: {pass_report}")
```

#### Custom Location

```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report

# Define custom observer location
austin_tx = {
    "name": "Austin, TX",
    "address": "Capitol Building",
    "latitude": 30.2672,
    "longitude": -97.7431,
    "elevation_m": 149,
}

# Generate report for Austin
data, report = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12),
    observer_location=austin_tx
)
```

#### Track Specific Satellites

```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report

# Track only BlueBird-6
satellites = {
    "BLUEBIRD-6": {
        "norad_id": 67232,
        "description": "Block 2 BlueBird satellite, launched Dec 2025",
    },
}

data, report = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12),
    satellites=satellites
)
```

#### Advanced: Use Individual Modules

```python
from ast_spacemobile.core.config import AST_SATELLITES, SIGNAL_PARAMS
from ast_spacemobile.core.tle import fetch_tle_data
from ast_spacemobile.core.calculations import calculate_signal_strength
from ast_spacemobile.analysis.passes import identify_passes

# Access configuration
print(f"Tracking {len(AST_SATELLITES)} satellites")
print(f"Frequency: {SIGNAL_PARAMS['frequency_ghz']} GHz")

# Fetch TLE for BlueBird-6
name, line1, line2 = fetch_tle_data(67232)
print(f"TLE: {name}")

# Calculate signal strength
signal = calculate_signal_strength(
    elevation_deg=45.0,  # degrees above horizon
    range_km=600.0,      # distance to satellite
    azimuth_deg=180.0    # south
)
print(f"SNR: {signal['snr_db']} dB")
print(f"Link Quality: {signal['link_quality']}")

# Process position data to find passes
# (assuming you have position_data from generate_satellite_passes)
# passes = identify_passes(position_data)
```

## Common Tasks

### View Current Satellite Catalog

```python
from ast_spacemobile import AST_SATELLITES

for name, info in AST_SATELLITES.items():
    print(f"{name}: NORAD {info['norad_id']}")
    print(f"  {info['description']}")
```

### Get Observer Location

```python
from ast_spacemobile import OBSERVER_LOCATION

print(f"Location: {OBSERVER_LOCATION['name']}")
print(f"Coordinates: {OBSERVER_LOCATION['latitude']}°N, "
      f"{abs(OBSERVER_LOCATION['longitude'])}°W")
print(f"Elevation: {OBSERVER_LOCATION['elevation_m']}m")
```

### Calculate Signal for Different Elevations

```python
from ast_spacemobile.core.calculations import calculate_signal_strength

elevations = [10, 30, 45, 60, 90]  # degrees
range_km = 600

print("Elevation | SNR (dB) | Link Quality")
print("-" * 40)
for elev in elevations:
    signal = calculate_signal_strength(elev, range_km, 0)
    print(f"{elev:8}° | {signal['snr_db']:7.2f} | {signal['link_quality']}")
```

## Examples Output

### Trajectory Report Example

```bash
python -m ast_spacemobile.cli.trajectory --start 2025-12-07 --end 2025-12-07
```

Output:
```
================================================================================
AST SPACEMOBILE SATELLITE TRAJECTORY AND SIGNAL STRENGTH REPORT
================================================================================
Location: Odessa, TX (1 Fairway Dr) (31.8457°N, 102.3676°W)
Elevation: 895 meters
Date Range: December 07, 2025 - December 07, 2025
Measurement Interval: 5 seconds
================================================================================

### SATELLITE INFORMATION ###

Processing: BLUEWALKER 3
  NORAD ID: 53807
  Description: Test satellite, largest commercial communications array in LEO
  TLE Data Retrieved: BLUEWALKER 3
  Calculating trajectories...
  ✓ Processed 17,280 data points
  ✓ Visible passes: 42.5 minutes total
  ✓ Maximum elevation: 67.23°

[... continues for all satellites ...]

✓ Detailed data saved to: ast_satellite_data_dec07-07.json
✓ CSV data saved to: ast_bluewalker_3_dec07-07.csv
[... more files ...]

✓ Comprehensive report saved to: AST_SpaceMobile_Satellite_Report_Dec07-07-2025.md
```

## Troubleshooting

### Import Error

```bash
# If you get "ModuleNotFoundError: No module named 'ast_spacemobile'"
pip install -e .
```

### Missing Dependencies

```bash
# If you get import errors for numpy, skyfield, etc.
pip install -r requirements.txt  # if exists, or:
pip install numpy pandas requests skyfield matplotlib
```

### Permission Error

```bash
# If pip fails due to permissions
pip install --user -e .
```

## Next Steps

- Read [README_LIBRARY.md](README_LIBRARY.md) for detailed documentation
- See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for migration from old scripts
- Check [BEFORE_AFTER.md](BEFORE_AFTER.md) for comparison
- Review [LIBRARY_SUMMARY.md](LIBRARY_SUMMARY.md) for complete overview

## Support

For help:
1. Check the documentation files
2. Review module docstrings: `help(ast_spacemobile)`
3. Look at examples in this guide
