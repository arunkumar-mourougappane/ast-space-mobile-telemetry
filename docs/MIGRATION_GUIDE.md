# Migration Guide: From Scripts to Library

This guide explains how the original scripts have been converted into a modularized library and how to use the new structure.

## What Changed?

The three original scripts have been consolidated into a well-organized library:

### Original Structure
```
ast_space_mobile_data/
├── ast_satellite_report.py      # ~547 lines - Trajectory calculations
├── generate_pass_report.py      # ~449 lines - Pass analysis
└── run_analysis.py               # ~190 lines - Pipeline orchestration
```

### New Library Structure
```
ast_space_mobile_data/
├── ast_spacemobile/              # Main library package
│   ├── __init__.py              # Public API
│   ├── core/                    # Core functionality
│   │   ├── config.py           # Configuration (satellites, locations, constants)
│   │   ├── tle.py              # TLE data fetching
│   │   └── calculations.py     # Trajectory & signal calculations
│   ├── analysis/                # Analysis tools
│   │   ├── passes.py           # Pass identification
│   │   └── visualization.py    # Graph generation
│   ├── reports/                 # Report generation
│   │   └── generator.py        # Report builders
│   └── cli/                     # Command-line interfaces
│       ├── trajectory.py       # Trajectory report CLI
│       ├── passes.py           # Pass analysis CLI
│       └── pipeline.py         # Full pipeline CLI
├── setup.py                     # Installation configuration
└── README_LIBRARY.md            # Library documentation
```

## Benefits of the New Structure

1. **Modularity**: Each component has a single responsibility
2. **Reusability**: Import only what you need
3. **Testability**: Each module can be tested independently
4. **Maintainability**: Changes are isolated to specific modules
5. **Distribution**: Can be installed as a package (`pip install -e .`)
6. **CLI Tools**: Three command-line tools available after installation

## Installation

```bash
# From the project directory
pip install -e .

# This creates three CLI commands:
# - ast-trajectory
# - ast-passes
# - ast-pipeline
```

## Usage Comparison

### 1. Trajectory Report Generation

#### Old Way
```bash
python ast_satellite_report.py --start 2025-12-07 --end 2025-12-12
```

#### New Way (CLI)
```bash
ast-trajectory --start 2025-12-07 --end 2025-12-12
```

#### New Way (Python API)
```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report

start = datetime(2025, 12, 7)
end = datetime(2025, 12, 12)
data, report = generate_trajectory_report(start, end)
```

### 2. Pass Analysis Report

#### Old Way
```bash
python generate_pass_report.py
```

#### New Way (CLI)
```bash
ast-passes
```

#### New Way (Python API)
```python
from ast_spacemobile import generate_pass_report

report = generate_pass_report()
```

### 3. Complete Pipeline

#### Old Way
```bash
python run_analysis.py --start 2025-12-07 --end 2025-12-12
```

#### New Way (CLI)
```bash
ast-pipeline --start 2025-12-07 --end 2025-12-12
```

## Advanced Usage Examples

### Custom Observer Location

```python
from ast_spacemobile import generate_trajectory_report
from datetime import datetime

# Define custom location
my_location = {
    "name": "Austin, TX",
    "address": "123 Main St",
    "latitude": 30.2672,
    "longitude": -97.7431,
    "elevation_m": 149,
}

# Generate report for custom location
data, report = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12),
    observer_location=my_location
)
```

### Custom Satellite List

```python
from ast_spacemobile import generate_trajectory_report
from datetime import datetime

# Track only specific satellites
my_satellites = {
    "BLUEWALKER 3": {
        "norad_id": 53807,
        "description": "Test satellite",
    },
    "BLUEBIRD-6": {
        "norad_id": 67232,
        "description": "Block 2 satellite",
    },
}

data, report = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12),
    satellites=my_satellites
)
```

### Using Individual Modules

```python
from ast_spacemobile.core.tle import fetch_tle_data
from ast_spacemobile.core.calculations import calculate_signal_strength
from ast_spacemobile.analysis.passes import identify_passes

# Fetch TLE data
name, line1, line2 = fetch_tle_data(53807)

# Calculate signal strength
metrics = calculate_signal_strength(
    elevation_deg=45.0,
    range_km=600.0,
    azimuth_deg=180.0
)
print(f"SNR: {metrics['snr_db']} dB")

# Identify passes from position data
passes = identify_passes(position_data)
```

## Configuration Updates

### Satellite Catalog

The satellite catalog has been updated with the latest NORAD IDs in `ast_spacemobile/core/config.py`:

```python
AST_SATELLITES = {
    "BLUEWALKER 3": {"norad_id": 53807, ...},
    "BLUEBIRD-A": {"norad_id": 61045, ...},  # Updated from 60399
    "BLUEBIRD-B": {"norad_id": 61046, ...},  # Updated from 60400
    "BLUEBIRD-C": {"norad_id": 61047, ...},  # Updated from 60401
    "BLUEBIRD-D": {"norad_id": 61048, ...},  # Updated from 60402
    "BLUEBIRD-E": {"norad_id": 61049, ...},  # Updated from 60403
    "BLUEBIRD-6": {"norad_id": 67232, ...},  # New! Launched Dec 2025
}
```

### Signal Parameters

All signal calculation parameters are now centralized in `ast_spacemobile/core/config.py`:

```python
SIGNAL_PARAMS = {
    "frequency_ghz": 2.0,
    "satellite_eirp_dbw": 55,
    "receiver_gain_dbi": 15,
    "system_losses_db": 3,
    "noise_floor_dbm": -110,
}
```

## Keeping Original Scripts (Optional)

If you want to keep the original scripts working, you can update them to use the library internally:

### Updated ast_satellite_report.py
```python
#!/usr/bin/env python3
from ast_spacemobile.cli.trajectory import main

if __name__ == "__main__":
    main()
```

### Updated generate_pass_report.py
```python
#!/usr/bin/env python3
from ast_spacemobile.cli.passes import main

if __name__ == "__main__":
    main()
```

### Updated run_analysis.py
```python
#!/usr/bin/env python3
from ast_spacemobile.cli.pipeline import main

if __name__ == "__main__":
    main()
```

## Testing the Installation

```bash
# Install the library
pip install -e .

# Test CLI tools
ast-trajectory --help
ast-passes --help
ast-pipeline --help

# Test Python import
python -c "from ast_spacemobile import generate_trajectory_report; print('Success!')"

# Run a quick analysis
ast-trajectory --start 2025-12-07 --end 2025-12-07
```

## Module Reference

### Core Modules

- **config.py**: Satellite catalog, observer location, signal parameters
- **tle.py**: TLE data fetching from Celestrak
- **calculations.py**: Trajectory and signal strength calculations

### Analysis Modules

- **passes.py**: Pass identification from position data
- **visualization.py**: Graph generation for passes

### Report Modules

- **generator.py**: Trajectory and pass report generation

### CLI Modules

- **trajectory.py**: Command-line interface for trajectory reports
- **passes.py**: Command-line interface for pass analysis
- **pipeline.py**: Command-line interface for full pipeline

## Next Steps

1. Install the library: `pip install -e .`
2. Try the CLI tools: `ast-trajectory --help`
3. Explore the Python API: See README_LIBRARY.md
4. Update any custom scripts to use the library modules
5. Consider adding tests in a `tests/` directory

## Support

For questions or issues:
- Check README_LIBRARY.md for detailed documentation
- Review the module docstrings for API details
- Open an issue if you encounter problems
