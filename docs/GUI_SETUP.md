# GTK GUI Setup Guide

This guide explains how to set up and run the AST SpaceMobile GTK graphical interface.

## Overview

The GTK GUI provides an interactive interface for satellite pass analysis with:
- Location selection (latitude, longitude, elevation)
- Date and time range picker
- Satellite dropdown selector
- Real-time telemetry data table
- Interactive visualization plots

## System Requirements

### Linux (Ubuntu/Debian)

Install GTK3 and PyGObject dependencies:

```bash
sudo apt-get update
sudo apt-get install -y \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    libgirepository1.0-dev \
    gcc \
    libcairo2-dev \
    pkg-config \
    python3-dev
```

### Fedora/RHEL

```bash
sudo dnf install -y \
    python3-gobject \
    gtk3 \
    gobject-introspection-devel \
    cairo-gobject-devel \
    pkg-config \
    python3-devel
```

### Arch Linux

```bash
sudo pacman -S python-gobject gtk3
```

### macOS

```bash
brew install pygobject3 gtk+3
```

### Windows

Windows setup is more complex. Recommended approach:

1. Install MSYS2 from https://www.msys2.org/
2. Open MSYS2 MinGW 64-bit terminal
3. Run:
```bash
pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject
```

## Python Package Installation

After installing system dependencies:

```bash
# Install PyGObject
pip install PyGObject

# Or install all project dependencies
pip install -e .
```

## Running the GUI

### Method 1: Direct Execution

```bash
python ast_spacemobile_gui.py
```

### Method 2: From Anywhere (if installed)

```bash
cd /path/to/ast_space_mobile_data
python ast_spacemobile_gui.py
```

## GUI Features

### 1. Observer Location

- **Latitude**: Enter latitude in degrees North (negative for South)
- **Longitude**: Enter longitude in degrees East (negative for West)
- **Elevation**: Enter elevation in meters above sea level

**Default**: Odessa, TX (31.8457°N, -102.3676°E, 895m)

### 2. Date and Time Range

- **Start Date**: YYYY-MM-DD format
- **Start Time**: HH:MM:SS format (24-hour)
- **End Date**: YYYY-MM-DD format
- **End Time**: HH:MM:SS format (24-hour)

All times are in UTC.

### 3. Satellite Selection

Choose from dropdown:
- BLUEWALKER 3
- BLUEBIRD-A through BLUEBIRD-E
- BLUEBIRD-6 (newest satellite)

### 4. Results

#### Pass Summary Tab
Shows table with:
- Pass number
- Start/end times
- Duration
- Maximum elevation
- Maximum signal power
- Average SNR

#### Detailed Data Tab
Shows 5-second interval data for passes:
- Timestamp
- Elevation, Azimuth, Range
- Signal power and SNR
- Link quality

#### Visualization Tab
Four plots showing:
- Elevation angle over time
- Received signal power over time
- Signal-to-Noise Ratio over time
- Satellite range over time

## Usage Example

1. **Set Location**:
   - Latitude: 40.7580 (New York City)
   - Longitude: -73.9855
   - Elevation: 10

2. **Set Time Range**:
   - Start: 2025-12-28 00:00:00
   - End: 2025-12-29 00:00:00

3. **Select Satellite**:
   - Choose "BLUEBIRD-6" from dropdown

4. **Generate**:
   - Click "Generate Analysis" button
   - Wait for TLE data fetch and calculation
   - View results in tabs

## Troubleshooting

### ImportError: cannot import name 'GLib' from 'gi.repository'

**Solution**: GTK3 system packages not installed. Follow system-specific installation above.

### Application window appears but crashes on Generate

**Problem**: Missing matplotlib backend support

**Solution**:
```bash
pip install --upgrade matplotlib
# Ensure GTK3 backend is available
```

### "Could not fetch TLE data"

**Problem**: No internet connection or CelesTrak is down

**Solution**: Application will use simulated TLE data automatically. For real data, check internet connection.

### GUI is very slow

**Problem**: Large date ranges generate lots of data

**Solution**:
- Limit analysis to 1-3 days
- Close and reopen if it becomes unresponsive
- The calculation runs in background but large datasets take time

### Window doesn't resize properly

**Solution**: Drag window borders or maximize the window. Minimum recommended size is 1200x800 pixels.

## Performance Tips

1. **Smaller Time Ranges**: 1-2 days is optimal for interactive use
2. **Single Satellite**: Analyze one satellite at a time
3. **Close Unused Tabs**: Switch to the tab you're viewing
4. **Clear Results**: Use "Clear Results" button between analyses

## Keyboard Shortcuts

- **Ctrl+Q**: Quit application (on some systems)
- **Tab**: Navigate between input fields
- **Enter**: Activate focused button
- **Escape**: Close dialog boxes

## Advanced Usage

### Batch Analysis

For analyzing multiple satellites or long time periods, consider using the CLI tools instead:

```bash
python -m ast_spacemobile.cli.trajectory --start 2025-12-01 --end 2025-12-31
```

### Export Data

Results are displayed in the GUI but not automatically saved. To save:
1. Use CLI tools for data export
2. Or take screenshots of plots
3. Or copy data from tables (Ctrl+C on selected rows)

## Known Limitations

1. **Single Satellite**: GUI analyzes one satellite at a time
2. **Memory Usage**: Large date ranges (>7 days) may use significant RAM
3. **No Export**: GUI doesn't save results directly (use CLI for that)
4. **UTC Only**: All times displayed in UTC (convert to local time manually)

## Getting Help

- **Documentation**: See [README_LIBRARY.md](README_LIBRARY.md)
- **Examples**: See [QUICK_START.md](QUICK_START.md)
- **CLI Alternative**: Use command-line tools for batch processing

## Development

To modify the GUI:

1. Edit `ast_spacemobile_gui.py`
2. Restart the application to see changes
3. GTK Inspector can help with debugging: `GTK_DEBUG=interactive python ast_spacemobile_gui.py`

---

**Last Updated**: 2025-12-28
**Version**: 1.0.0
