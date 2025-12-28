# AST SpaceMobile Satellite Analysis

A comprehensive Python library for tracking and analyzing AST SpaceMobile satellite trajectories, signal strength, and pass predictions.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This project provides tools to:
- Track all **7 AST SpaceMobile satellites** (BlueWalker 3 + BlueBird constellation including new BlueBird-6)
- Calculate satellite trajectories and positions using SGP4 propagator
- Estimate signal strength and link quality based on link budget analysis
- Identify and analyze individual satellite passes
- Generate detailed reports with visualizations
- Export data in multiple formats (JSON, CSV, Markdown, PDF)

## Quick Start

### Installation

```bash
# Clone or navigate to the repository
cd ast_space_mobile_data

# Install the library
pip install -e .
```

### Basic Usage

#### Command Line

```bash
# Generate trajectory report
python -m ast_spacemobile.cli.trajectory --start 2025-12-07 --end 2025-12-12

# Generate pass analysis report
python -m ast_spacemobile.cli.passes

# Run complete analysis pipeline
python -m ast_spacemobile.cli.pipeline
```

#### Python API

```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report

# Generate report for a date range
data, report = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12)
)
```

See **[Quick Start Guide](docs/QUICK_START.md)** and **[examples/](examples/)** for more usage patterns.

## Features

### Satellite Tracking
- **7 Satellites**: BlueWalker 3 + BlueBird A-E (Block 1) + BlueBird-6 (Block 2)
- **Real-time TLE**: Fetches latest orbital parameters from CelesTrak
- **Accurate Propagation**: Uses SGP4 via Skyfield library
- **Updated Catalog**: Includes latest NORAD IDs (BlueBird-6 launched Dec 2025)

### Signal Analysis
- **Link Budget Calculation**: Estimates received power and SNR
- **Path Loss Modeling**: Free space + atmospheric attenuation
- **Quality Assessment**: Categorizes link quality (Excellent/Good/Fair/Poor)
- **Configurable Parameters**: Customizable frequency, EIRP, gain settings

### Visualization & Reports
- **Pass Graphs**: Signal strength and elevation profiles
- **Detailed Reports**: Comprehensive markdown reports with statistics
- **CSV Export**: Raw data for further analysis
- **PDF Generation**: Professional reports (via legacy scripts)

## Project Structure

```
ast_space_mobile_data/
├── ast_spacemobile/          # Main library package
│   ├── core/                 # Core functionality
│   │   ├── config.py        # Satellite catalog & configuration
│   │   ├── tle.py           # TLE data fetching
│   │   └── calculations.py  # Trajectory & signal calculations
│   ├── analysis/             # Analysis tools
│   │   ├── passes.py        # Pass identification
│   │   └── visualization.py # Graph generation
│   ├── reports/              # Report generation
│   │   └── generator.py     # Report builders
│   └── cli/                  # Command-line interfaces
│       ├── trajectory.py    # Trajectory report CLI
│       ├── passes.py        # Pass analysis CLI
│       └── pipeline.py      # Full pipeline CLI
├── docs/                     # Documentation
│   ├── README_LIBRARY.md    # Complete library documentation
│   ├── QUICK_START.md       # Quick reference guide
│   ├── MIGRATION_GUIDE.md   # Migration from old scripts
│   └── LIBRARY_SUMMARY.md   # Project overview
├── examples/                 # Usage examples
│   ├── basic_trajectory.py  # Simple trajectory report
│   ├── custom_location.py   # Custom observer location
│   ├── signal_analysis.py   # Signal strength analysis
│   └── track_single_satellite.py  # Single satellite tracking
├── scripts/                  # Legacy scripts (backward compatibility)
│   ├── ast_satellite_report.py
│   ├── generate_pass_report.py
│   ├── run_analysis.py
│   └── generate_pdf_report.py
├── tests/                    # Unit tests
├── setup.py                  # Package configuration
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Satellite Catalog

The library tracks the following AST SpaceMobile satellites:

| Satellite | NORAD ID | Description | Launch Date |
|-----------|----------|-------------|-------------|
| BlueWalker 3 | 53807 | Test satellite, largest commercial array | Sep 2022 |
| BlueBird-A | 61045 | Block 1 (SPACEMOBILE-003) | Sep 2024 |
| BlueBird-B | 61046 | Block 1 (SPACEMOBILE-005) | Sep 2024 |
| BlueBird-C | 61047 | Block 1 (SPACEMOBILE-001) | Sep 2024 |
| BlueBird-D | 61048 | Block 1 (SPACEMOBILE-002) | Sep 2024 |
| BlueBird-E | 61049 | Block 1 (SPACEMOBILE-004) | Sep 2024 |
| **BlueBird-6** | **67232** | **Block 2 (FM1), 10x capacity** | **Dec 2025** ✨ NEW |

## Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running quickly
- **[Library Documentation](docs/README_LIBRARY.md)** - Complete API reference
- **[Migration Guide](docs/MIGRATION_GUIDE.md)** - Upgrade from legacy scripts
- **[Before & After](docs/BEFORE_AFTER.md)** - See the improvements
- **[Examples](examples/)** - Code examples and usage patterns

## Requirements

- Python >= 3.8
- numpy >= 1.20.0
- pandas >= 1.3.0
- requests >= 2.26.0
- skyfield >= 1.42
- matplotlib >= 3.4.0

All dependencies are automatically installed with `pip install -e .`

## Usage Examples

### Example 1: Generate Trajectory Report

```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report

# Generate report
data, report_file = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12)
)

print(f"Report saved to: {report_file}")
```

### Example 2: Custom Observer Location

```python
from datetime import datetime
from ast_spacemobile import generate_trajectory_report

# Define custom location
location = {
    "name": "San Francisco",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "elevation_m": 16,
}

# Generate report for custom location
data, report = generate_trajectory_report(
    start_date=datetime(2025, 12, 7),
    end_date=datetime(2025, 12, 12),
    observer_location=location
)
```

### Example 3: Signal Strength Analysis

```python
from ast_spacemobile.core.calculations import calculate_signal_strength

# Calculate signal at 45° elevation, 600 km range
signal = calculate_signal_strength(45.0, 600.0, 180.0)

print(f"SNR: {signal['snr_db']} dB")
print(f"Link Quality: {signal['link_quality']}")
```

See **[examples/](examples/)** for more detailed examples.

## Command-Line Tools

### Trajectory Report
```bash
python -m ast_spacemobile.cli.trajectory --start 2025-12-01 --end 2025-12-15
```

### Pass Analysis
```bash
python -m ast_spacemobile.cli.passes --output-dir my_graphs
```

### Complete Pipeline
```bash
python -m ast_spacemobile.cli.pipeline --start 2025-12-01 --end 2025-12-15
```

## Output Files

- **JSON**: `ast_satellite_data_<dates>.json` - Complete trajectory data
- **CSV**: `ast_<satellite>_<dates>.csv` - Per-satellite data
- **Markdown**: `AST_SpaceMobile_*_Report.md` - Human-readable reports
- **Graphs**: `pass_graphs/*.png` - Signal strength visualizations

## Key Features of Modular Library

✅ **Clean Architecture**: Separated concerns with core, analysis, and reporting modules
✅ **Reusable Components**: Import only what you need
✅ **Multiple Interfaces**: Both CLI and Python API
✅ **Well Documented**: Comprehensive docs and examples
✅ **Tested**: Verified working with all components
✅ **Extensible**: Easy to add new satellites or analysis methods
✅ **Updated Data**: Latest NORAD IDs including BlueBird-6

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black ast_spacemobile/
isort ast_spacemobile/
flake8 ast_spacemobile/
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided for analysis and educational purposes.

## Acknowledgments

- **TLE Data**: [CelesTrak](https://celestrak.org/)
- **Orbital Mechanics**: [Skyfield](https://rhodesmill.org/skyfield/)
- **Satellite Info**: Public AST SpaceMobile sources

## Support

- **Documentation**: See [docs/](docs/)
- **Examples**: See [examples/](examples/)
- **Quick Start**: See [docs/QUICK_START.md](docs/QUICK_START.md)
- **Issues**: Open an issue in the repository

## Version

**Current Version**: 1.0.0
**Last Updated**: 2025-12-28

## What's New

- ✨ **Modular library structure** with clean API
- ✨ **BlueBird-6 satellite** added (NORAD 67232, launched Dec 2025)
- ✨ **Updated NORAD IDs** for BlueBird A-E constellation
- ✨ **Python API** in addition to CLI tools
- ✨ **Comprehensive documentation** and examples
- ✨ **Installable package** via pip

---

**Note**: This library uses the latest satellite NORAD IDs updated December 2025, including the newly launched BlueBird-6 Block 2 satellite with 10x capacity.
