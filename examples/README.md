# Examples

This directory contains example scripts demonstrating how to use the AST SpaceMobile library.

## Available Examples

### Basic Usage

- **[basic_trajectory.py](basic_trajectory.py)** - Generate a simple trajectory report
- **[fetch_tle.py](fetch_tle.py)** - Fetch TLE data for all satellites

### Customization

- **[custom_location.py](custom_location.py)** - Generate reports for custom observer locations
- **[track_single_satellite.py](track_single_satellite.py)** - Track only specific satellites

### Analysis

- **[signal_analysis.py](signal_analysis.py)** - Analyze signal strength at different elevations

## Running Examples

Make sure the library is installed:

```bash
pip install -e .
```

Then run any example:

```bash
python examples/basic_trajectory.py
python examples/signal_analysis.py
python examples/custom_location.py
```

## Creating Your Own Scripts

Use these examples as templates for your own analysis scripts. The library provides:

- **Configuration**: `from ast_spacemobile.core.config import AST_SATELLITES, OBSERVER_LOCATION`
- **TLE Fetching**: `from ast_spacemobile.core.tle import fetch_tle_data`
- **Calculations**: `from ast_spacemobile.core.calculations import calculate_signal_strength`
- **Report Generation**: `from ast_spacemobile import generate_trajectory_report, generate_pass_report`

See the [library documentation](../docs/README_LIBRARY.md) for complete API reference.
