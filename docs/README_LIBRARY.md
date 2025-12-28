# AST SpaceMobile Analysis Library

A modular Python library for analyzing AST SpaceMobile satellite trajectories and signal strength over specified locations and time periods.

## Features

- **Satellite Tracking**: Track all AST SpaceMobile satellites (BlueWalker 3, BlueBird A-E, BlueBird-6)
- **Trajectory Calculations**: Calculate satellite positions using Skyfield and SGP4 propagator
- **Signal Strength Analysis**: Estimate received power, SNR, and link quality
- **Pass Identification**: Automatically identify and analyze individual satellite passes
- **Visualization**: Generate detailed graphs of signal strength and elevation profiles
- **Report Generation**: Create comprehensive markdown reports with statistics and visualizations

## Installation

### From Source

```bash
# Clone the repository or navigate to the project directory
cd ast_space_mobile_data

# Install in development mode
pip install -e .
```

### Dependencies

- Python >= 3.8
- numpy >= 1.20.0
- pandas >= 1.3.0
- requests >= 2.26.0
- skyfield >= 1.42
- matplotlib >= 3.4.0

## Quick Start

### Command Line Interface

After installation, three command-line tools are available:

#### 1. Generate Trajectory Report

```bash
# Use default dates (Dec 7-12, 2025)
ast-trajectory

# Custom date range
ast-trajectory --start 2025-12-01 --end 2025-12-15

# Single day analysis
ast-trajectory --start 2025-12-10 --end 2025-12-10
```

#### 2. Generate Pass Analysis Report

```bash
# Auto-detect latest satellite data file
ast-passes

# Specify satellite data file
ast-passes --data ast_satellite_data_dec7-12.json

# Custom output directory for graphs
ast-passes --output-dir my_graphs
```

#### 3. Run Complete Pipeline

```bash
# Run full analysis pipeline
ast-pipeline

# Custom date range
ast-pipeline --start 2025-12-01 --end 2025-12-15

# Skip certain steps
ast-pipeline --skip-data  # Use existing data
ast-pipeline --skip-passes  # Use existing pass report
ast-pipeline --skip-pdf  # Skip PDF generation
```

### Python API

```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report, generate_pass_report

# Generate trajectory report
start_date = datetime(2025, 12, 7)
end_date = datetime(2025, 12, 12)
satellite_data, report_file = generate_trajectory_report(start_date, end_date)

# Generate pass analysis report
pass_report_file = generate_pass_report()
```

### Advanced Usage

```python
from ast_spacemobile.core.config import AST_SATELLITES, OBSERVER_LOCATION
from ast_spacemobile.core.tle import fetch_tle_data
from ast_spacemobile.core.calculations import calculate_signal_strength, generate_satellite_passes
from ast_spacemobile.analysis.passes import identify_passes
from skyfield.api import EarthSatellite, load, wgs84

# Fetch TLE data for a satellite
name, line1, line2 = fetch_tle_data(53807)  # BlueWalker 3

# Create satellite object
ts = load.timescale()
satellite = EarthSatellite(line1, line2, name, ts)

# Create observer location
observer = wgs84.latlon(
    OBSERVER_LOCATION['latitude'],
    OBSERVER_LOCATION['longitude'],
    OBSERVER_LOCATION['elevation_m']
)

# Generate satellite positions
from datetime import datetime, timedelta
start = datetime(2025, 12, 7)
end = datetime(2025, 12, 8)
positions = generate_satellite_passes(satellite, observer, start, end)

# Identify passes
passes = identify_passes(positions)

# Calculate signal strength for a specific position
elevation = 45.0  # degrees
range_km = 600.0
azimuth = 180.0
signal_metrics = calculate_signal_strength(elevation, range_km, azimuth)
print(f"SNR: {signal_metrics['snr_db']} dB")
print(f"Link Quality: {signal_metrics['link_quality']}")
```

## Library Structure

```
ast_spacemobile/
├── __init__.py              # Main library interface
├── core/                    # Core functionality
│   ├── config.py           # Configuration and constants
│   ├── tle.py              # TLE data fetching
│   └── calculations.py     # Trajectory and signal calculations
├── analysis/                # Analysis functionality
│   ├── passes.py           # Pass identification
│   └── visualization.py    # Graph generation
├── reports/                 # Report generation
│   └── generator.py        # Report builders
└── cli/                     # Command-line interfaces
    ├── trajectory.py       # Trajectory report CLI
    ├── passes.py           # Pass analysis CLI
    └── pipeline.py         # Full pipeline CLI
```

## Configuration

### Satellites

The library tracks the following AST SpaceMobile satellites by default:

- **BlueWalker 3** (NORAD 53807) - Test satellite
- **BlueBird-A** (NORAD 61045) - Block 1 satellite
- **BlueBird-B** (NORAD 61046) - Block 1 satellite
- **BlueBird-C** (NORAD 61047) - Block 1 satellite
- **BlueBird-D** (NORAD 61048) - Block 1 satellite
- **BlueBird-E** (NORAD 61049) - Block 1 satellite
- **BlueBird-6** (NORAD 67232) - Block 2 satellite (10x capacity)

Satellite configuration can be found in `ast_spacemobile/core/config.py`.

### Observer Location

Default observer location is Odessa, TX (1 Fairway Dr):
- Latitude: 31.8457°N
- Longitude: 102.3676°W
- Elevation: 895m

You can customize the observer location by passing a custom `observer_location` dictionary to the report generation functions.

### Signal Parameters

Signal calculation parameters can be customized in `ast_spacemobile/core/config.py`:

```python
SIGNAL_PARAMS = {
    "frequency_ghz": 2.0,
    "satellite_eirp_dbw": 55,
    "receiver_gain_dbi": 15,
    "system_losses_db": 3,
    "noise_floor_dbm": -110,
}
```

## Output Files

### Trajectory Report

- `ast_satellite_data_<dates>.json` - Complete trajectory data
- `ast_<satellite>_<dates>.csv` - Per-satellite CSV data
- `AST_SpaceMobile_Satellite_Report_<dates>.md` - Markdown report

### Pass Analysis Report

- `AST_SpaceMobile_Detailed_Pass_Report.md` - Detailed pass analysis
- `pass_graphs/*.png` - Signal strength graphs for each pass

## Backward Compatibility

The original scripts (`ast_satellite_report.py`, `generate_pass_report.py`, `run_analysis.py`) can be updated to use the new library while maintaining their CLI interfaces. See the "Migration Guide" section below.

## Migration Guide

To update existing scripts to use the library:

### Old Way (ast_satellite_report.py)
```python
# All functionality embedded in script
if __name__ == "__main__":
    # Parse args and generate report
```

### New Way
```python
from ast_spacemobile import generate_trajectory_report

if __name__ == "__main__":
    # Parse args
    data, report = generate_trajectory_report(start_date, end_date)
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Code Style

```bash
# Format code
black ast_spacemobile/
isort ast_spacemobile/

# Lint code
flake8 ast_spacemobile/
bandit -r ast_spacemobile/
```

## Contributing

Contributions are welcome! Please ensure:

1. Code follows PEP 8 style guidelines
2. All tests pass
3. New features include tests and documentation
4. Security issues are addressed (run bandit)

## License

This project is provided for analysis and educational purposes.

## Acknowledgments

- TLE data provided by [CelesTrak](https://celestrak.org/)
- Orbital mechanics calculations using [Skyfield](https://rhodesmill.org/skyfield/)
- AST SpaceMobile satellite information from public sources

## Support

For questions or issues, please open an issue in the project repository.

## Version History

### 1.0.0 (2025-12-28)
- Initial modular library release
- Separated core functionality into reusable modules
- Added CLI entry points
- Comprehensive documentation
- Updated satellite catalog with latest BlueBird satellites
