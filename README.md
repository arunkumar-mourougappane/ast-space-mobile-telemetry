# AST SpaceMobile Satellite Telemetry Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Comprehensive trajectory and signal strength analysis toolkit for AST SpaceMobile satellite constellation. This project generates detailed reports, visualizations, and datasets for satellite passes over any location with configurable date ranges.

**Key Features:**

- 🛰️ Tracks all 6 AST SpaceMobile satellites (BlueWalker 3, BlueBird 1-5)
- 📅 Configurable date ranges for custom analysis periods
- 📊 Detailed pass-by-pass analysis with complete position data
- 📈 Signal strength graphs for every satellite pass
- 📕 Professional PDF reports with embedded visualizations
- 💾 Export to CSV/JSON for custom analysis
- 🎯 5-second measurement intervals for high precision

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/arunkumar-mourougappane/ast-space-mobile-telemetry.git
cd ast-space-mobile-telemetry

# Run the automated setup script
./setup_venv.sh
# or on Windows/cross-platform:
python setup_venv.py

# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### Basic Usage

```bash
# Run complete analysis with default dates (Dec 7-12, 2025)
python run_analysis.py

# Custom date range
python run_analysis.py --start 2025-12-01 --end 2025-12-31

# Generate only satellite data
python ast_satellite_report.py --start 2025-12-15 --end 2025-12-20

# View all available options
python run_analysis.py --help
```

## Project Structure

```text
ast-space-mobile-telemetry/
├── ast_satellite_report.py      # Satellite data generation & TLE fetching
├── generate_pass_report.py      # Pass analysis & visualization
├── generate_pdf_report.py       # PDF report generation
├── run_analysis.py              # Complete pipeline runner
├── setup_venv.sh               # Virtual environment setup (bash)
├── setup_venv.py               # Virtual environment setup (Python)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── LICENSE                     # MIT License
```

## Generated Output Files

Running the analysis pipeline generates the following files:

## Output File Descriptions

### 📊 Reports

#### 1. PDF Report (`AST_SpaceMobile_Detailed_Pass_Report.pdf`)

- **Size:** ~34 MB (with 228 embedded graphs)
- Professional layout with title page and styling
- All satellite passes with complete position data tables
- High-resolution embedded graphs
- Color-coded tables and quality indicators
- Optimized for printing and distribution

#### 2. Markdown Report (`AST_SpaceMobile_Detailed_Pass_Report.md`)

- **Size:** ~1.3 MB
- Complete source document
- Full position data for all passes (every 5-second measurement)
- Links to embedded graph images
- Easy to parse and customize

#### 3. Executive Summary (`AST_SpaceMobile_Satellite_Report_*.md`)

- Fleet overview and orbital parameters
- TLE data for each satellite
- Aggregate statistics
- Methodology documentation

### 📈 Visualizations

**`pass_graphs/` directory** - Signal strength graphs for each pass

- One graph per satellite pass
- Dual-panel layout:
  - Top: Signal power (dBm) and elevation angle
  - Bottom: SNR with quality threshold lines
- **Format:** PNG (150 DPI)
- **Typical size:** ~140 KB per graph

### 📁 Data Files

#### CSV Files (5-second interval data)

- One file per satellite: `ast_[satellite_name]_[daterange].csv`
- **Columns:** timestamp, elevation, azimuth, range, signal power, SNR, link quality, and more
- **Records:** ~103,680 per satellite for 6-day analysis
- **Format:** Standard CSV, easily imported into Excel, Python, R, etc.

#### JSON File

- `ast_satellite_data_[daterange].json`
- Complete structured dataset with all position data
- Includes satellite info, TLE data, and position arrays
- **Format:** Hierarchical JSON structure

## Analysis Capabilities

### What You Can Do With This Data

1. **Pass Prediction**
   - Identify when satellites will be visible
   - Find optimal communication windows
   - Plan antenna pointing schedules

2. **Link Budget Analysis**
   - Estimate received signal strength
   - Calculate signal-to-noise ratios
   - Assess link quality and reliability

3. **Coverage Analysis**
   - Determine satellite visibility patterns
   - Analyze elevation angles and durations
   - Compare performance across satellites

4. **Custom Processing**
   - Import CSV data into your analysis tools
   - Build custom visualizations
   - Integrate with other datasets

## Sample Analysis Results (Dec 7-12, 2025)

### Satellites Tracked

| Satellite        | NORAD ID | Passes  | Description                                                 |
| ---------------- | -------- | ------- | ----------------------------------------------------------- |
| **BLUEWALKER 3** | 53807    | 45      | Test satellite, largest commercial LEO communications array |
| **BLUEBIRD-1**   | 60399    | 36      | First commercial Block 1 BlueBird satellite                 |
| **BLUEBIRD-2**   | 60400    | 37      | Second commercial Block 1 BlueBird satellite                |
| **BLUEBIRD-3**   | 60401    | 37      | Third commercial Block 1 BlueBird satellite                 |
| **BLUEBIRD-4**   | 60402    | 37      | Fourth commercial Block 1 BlueBird satellite                |
| **BLUEBIRD-5**   | 60403    | 36      | Fifth commercial Block 1 BlueBird satellite                 |
| **TOTAL**        | -        | **228** | All satellites combined                                     |

### Key Statistics

**Location:** Midland, TX (31.9973°N, 102.0779°W, elevation 872m)

- **Analysis Duration:** 6 days
- **Measurement Interval:** 5 seconds
- **Total Data Points:** 622,086 across all satellites
- **Total Passes:** 228 individual satellite passes
- **Peak Signal Strength:** -54 to -57 dBm (closest approaches)
- **Maximum Elevations:** 73-87° (excellent overhead passes)
- **SNR Range:** 33-53 dB during visible passes
- **Link Quality:** Predominantly "Excellent" to "Good"

## Technical Details

### Dependencies

- **Python 3.8+** required
- **Core Libraries:**
  - `skyfield` - Satellite orbital mechanics (SGP4 propagator)
  - `numpy` - Numerical computations
  - `pandas` - Data manipulation and CSV export
  - `matplotlib` - Graph generation
  - `requests` - TLE data fetching
  - `markdown` - Report generation
  - `weasyprint` - PDF generation

See [requirements.txt](requirements.txt) for complete list with versions.

### Signal Strength Model

**Calculation Method:**

- **Frequency:** ~2 GHz (AST SpaceMobile cellular bands)
- **Free Space Path Loss:** FSPL(dB) = 20×log₁₀(distance_km) + 20×log₁₀(frequency_MHz) + 32.45
- **Atmospheric Attenuation:** Elevation-dependent (2-7 dB)
- **Satellite EIRP:** 55 dBW (assumed based on typical LEO satcom)
- **Ground Station Gain:** 15 dBi
- **System Losses:** 3 dB (cables, connectors)
- **Noise Floor:** -110 dBm

**Link Quality Thresholds:**

- **Excellent:** SNR ≥ 20 dB - Full data throughput
- **Good:** SNR ≥ 15 dB - High reliability
- **Fair:** SNR ≥ 10 dB - Acceptable performance
- **Poor:** SNR ≥ 5 dB - Marginal link
- **Very Poor:** SNR < 5 dB - Unreliable

### Orbital Mechanics

- **TLE Data Source:** Celestrak (<https://celestrak.org>)
- **Propagator:** SGP4 (Simplified General Perturbations 4)
- **Library:** Skyfield (Python)
- **Precision:** Sub-kilometer accuracy for trajectory calculations
- **Update Frequency:** TLE data is fetched fresh for each analysis run

### Data Collection Process

1. **TLE Fetching:** Query Celestrak for latest orbital elements
2. **Trajectory Calculation:** Propagate satellite positions using SGP4
3. **Topocentric Conversion:** Calculate elevation, azimuth, range from observer
4. **Signal Estimation:** Apply link budget model to each measurement
5. **Pass Identification:** Detect continuous visibility periods
6. **Visualization:** Generate graphs for each identified pass
7. **Report Generation:** Compile markdown and PDF reports

## Detailed Usage Examples

### 1. Complete Pipeline with Default Settings

```bash
# Generates data for Dec 7-12, 2025 over Midland, TX
python run_analysis.py
```

This will:

- Fetch TLE data for all 6 satellites
- Calculate trajectories at 5-second intervals
- Identify and analyze all satellite passes
- Generate 228 signal strength graphs
- Create markdown and PDF reports

**Output:**

- `ast_satellite_data_dec7-12.json` (268 MB)
- `ast_*_dec7-12.csv` (6 files, 9.8 MB each)
- `AST_SpaceMobile_Detailed_Pass_Report.md` (1.3 MB)
- `AST_SpaceMobile_Detailed_Pass_Report.pdf` (34 MB)
- `pass_graphs/*.png` (228 images)

### 2. Custom Date Range Analysis

```bash
# Analyze entire month of December
python run_analysis.py --start 2025-12-01 --end 2025-12-31

# Single day analysis
python run_analysis.py --start 2025-12-25 --end 2025-12-25

# Week-long analysis
python run_analysis.py --start 2025-12-15 --end 2025-12-21
```

### 3. Partial Pipeline Execution

```bash
# Only generate satellite data (skip report generation)
python ast_satellite_report.py --start 2025-12-10 --end 2025-12-15

# Only generate pass report from existing data
python run_analysis.py --skip-data

# Regenerate PDF only
python run_analysis.py --skip-data --skip-passes

# Skip PDF generation
python run_analysis.py --skip-pdf
```

### 4. Using Individual Scripts

```bash
# Step 1: Generate satellite trajectory data
python ast_satellite_report.py --start 2025-12-07 --end 2025-12-12

# Step 2: Analyze passes and create visualizations
python generate_pass_report.py

# Step 3: Generate professional PDF
python generate_pdf_report.py
```

## Command-Line Options

### run_analysis.py

| Option | Description | Default |
|--------|-------------|---------|
| `--start DATE` | Start date (YYYY-MM-DD) | 2025-12-07 |
| `--end DATE` | End date (YYYY-MM-DD) | 2025-12-12 |
| `--skip-data` | Skip satellite data generation | False |
| `--skip-passes` | Skip pass report generation | False |
| `--skip-pdf` | Skip PDF generation | False |

### ast_satellite_report.py

| Option | Description | Default |
|--------|-------------|---------|
| `--start DATE` | Start date (YYYY-MM-DD) | 2025-12-07 |
| `--end DATE` | End date (YYYY-MM-DD) | 2025-12-12 |

### generate_pass_report.py

| Option | Description | Default |
|--------|-------------|---------|
| `--input FILE` | Input JSON data file | ast_satellite_data_dec7-12.json |
| `--auto` | Auto-detect latest data file | False |

## Configuration

### Location

By default, the analysis is performed for **Midland, TX**. To analyze a different location, modify the `MIDLAND_TX` constant in `ast_satellite_report.py`:

```python
MIDLAND_TX = {
    "latitude": 31.9973,    # Your latitude
    "longitude": -102.0779, # Your longitude
    "elevation_m": 872      # Elevation in meters
}
```

### Measurement Interval

Default is 5 seconds. To change, modify the `interval_seconds` parameter in the `generate_satellite_passes()` call.

## CSV Data Format

Each CSV file contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | string | ISO 8601 UTC timestamp |
| `unix_timestamp` | float | Unix epoch time |
| `elevation_deg` | float | Satellite elevation angle (degrees above horizon) |
| `azimuth_deg` | float | Satellite azimuth angle (degrees, 0°=North) |
| `range_km` | float | Distance from observer to satellite (km) |
| `satellite_lat` | float | Satellite sub-point latitude (degrees) |
| `satellite_lon` | float | Satellite sub-point longitude (degrees) |
| `satellite_alt_km` | float | Satellite altitude above Earth (km) |
| `visible` | boolean | True if satellite is above horizon |
| `received_power_dbm` | float | Estimated received signal power (dBm) |
| `snr_db` | float | Signal-to-Noise Ratio (dB) |
| `link_quality` | string | Qualitative assessment (Excellent/Good/Fair/Poor/Very Poor) |
| `path_loss_db` | float | Total path loss (dB) |
| `atmospheric_loss_db` | float | Atmospheric attenuation (dB) |

## Troubleshooting

### Common Issues

**Problem:** `ModuleNotFoundError` when running scripts

**Solution:** Make sure virtual environment is activated and dependencies are installed:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Problem:** TLE data fetch fails

**Solution:** Check internet connection. The scripts require access to celestrak.org to download current orbital elements.

**Problem:** PDF generation fails

**Solution:** Ensure weasyprint dependencies are installed. On Linux:

```bash
sudo apt-get install python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**Problem:** Analysis takes too long

**Solution:** Reduce date range or increase measurement interval. Analysis time scales with duration and sample rate.

## Performance Notes

- **Memory Usage:** ~2-3 GB RAM for 6-day analysis
- **Processing Time:**
  - Satellite data generation: ~2-3 minutes
  - Pass analysis and graphs: ~3-5 minutes
  - PDF generation: ~2-3 minutes
- **Disk Space:**
  - Complete 6-day analysis: ~350 MB
  - Per day: ~60 MB

## Contributing

Contributions are welcome! Areas for improvement:

- Additional signal propagation models
- Support for more satellite constellations
- Interactive web-based visualizations
- Real-time tracking capabilities
- Additional output formats

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **AST SpaceMobile** for satellite constellation data
- **Celestrak** for TLE data distribution
- **Skyfield** library by Brandon Rhodes
- Python scientific computing community

## References

- [AST SpaceMobile](https://ast-science.com/)
- [Celestrak](https://celestrak.org/)
- [Skyfield Documentation](https://rhodesmill.org/skyfield/)
- [SGP4 Propagator](https://en.wikipedia.org/wiki/Simplified_perturbations_models)

## Contact

For questions, issues, or suggestions:

- Open an issue on [GitHub](https://github.com/arunkumar-mourougappane/ast-space-mobile-telemetry/issues)
- Check existing documentation in generated reports

---

**Generated with ❤️ for satellite analysis and space telecommunications**
