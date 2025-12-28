"""
Report generation functionality
Creates markdown and JSON reports for satellite trajectory and pass analysis
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from skyfield.api import EarthSatellite, load, wgs84

from ast_spacemobile.core.config import AST_SATELLITES, OBSERVER_LOCATION
from ast_spacemobile.core.tle import fetch_tle_data, create_simulated_tle
from ast_spacemobile.core.calculations import generate_satellite_passes
from ast_spacemobile.analysis.passes import identify_passes
from ast_spacemobile.analysis.visualization import (
    create_signal_strength_graph,
    utc_to_cst,
    format_duration,
)


def generate_trajectory_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    satellites: Optional[Dict] = None,
    observer_location: Optional[Dict] = None,
) -> Tuple[Dict, str]:
    """
    Generate comprehensive satellite trajectory and signal strength report

    Args:
        start_date: Start date for analysis (defaults to Dec 7, 2025)
        end_date: End date for analysis (defaults to Dec 12, 2025)
        satellites: Dictionary of satellites to track (defaults to AST_SATELLITES)
        observer_location: Observer location dict (defaults to OBSERVER_LOCATION)

    Returns:
        Tuple of (satellite_data_dict, report_filename)
    """
    # Set defaults
    if start_date is None:
        start_date = datetime(2025, 12, 7, 0, 0, 0)
    if end_date is None:
        end_date = datetime(2025, 12, 12, 23, 59, 59)
    if satellites is None:
        satellites = AST_SATELLITES
    if observer_location is None:
        observer_location = OBSERVER_LOCATION

    print("=" * 80)
    print("AST SPACEMOBILE SATELLITE TRAJECTORY AND SIGNAL STRENGTH REPORT")
    print("=" * 80)
    print(
        f"Location: {observer_location['name']} ({observer_location['address']}) "
        f"({observer_location['latitude']}°N, {abs(observer_location['longitude'])}°W)"
    )
    print(f"Elevation: {observer_location['elevation_m']} meters")
    print(f"Date Range: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    print("Measurement Interval: 5 seconds")
    print("=" * 80)
    print()

    # Load timescale
    ts = load.timescale()

    # Create observer location
    observer = wgs84.latlon(
        observer_location["latitude"],
        observer_location["longitude"],
        observer_location["elevation_m"],
    )

    all_satellite_data = {}
    report_sections = []

    print("\n### SATELLITE INFORMATION ###\n")

    for sat_name, sat_info in satellites.items():
        print(f"\nProcessing: {sat_name}")
        print(f"  NORAD ID: {sat_info['norad_id']}")
        print(f"  Description: {sat_info['description']}")

        # Fetch TLE data
        name, line1, line2 = fetch_tle_data(sat_info["norad_id"])

        if not line1 or not line2:
            print(f"  ⚠ WARNING: Could not fetch TLE data for {sat_name}")
            print("  Using simulated data for demonstration purposes")
            name, line1, line2 = create_simulated_tle(sat_info["norad_id"], sat_name)

        print(f"  TLE Data Retrieved: {name}")

        # Create satellite object
        satellite = EarthSatellite(line1, line2, name, ts)

        # Generate trajectory data
        print("  Calculating trajectories...")
        positions = generate_satellite_passes(satellite, observer, start_date, end_date, interval_seconds=5)

        all_satellite_data[sat_name] = {
            "info": sat_info,
            "tle": {"name": name, "line1": line1, "line2": line2},
            "positions": positions,
        }

        # Calculate statistics
        visible_positions = [p for p in positions if p["visible"]]

        if visible_positions:
            avg_elevation_visible = np.mean([p["elevation_deg"] for p in visible_positions])
            max_elevation_visible = max([p["elevation_deg"] for p in visible_positions])
            total_visible_time = len(visible_positions) * 5 / 60  # minutes

            # Signal statistics for visible passes
            signal_powers = [p["received_power_dbm"] for p in visible_positions if p["received_power_dbm"] is not None]
            if signal_powers:
                avg_signal_power = np.mean(signal_powers)
                max_signal_power = max(signal_powers)
            else:
                avg_signal_power = None
                max_signal_power = None
        else:
            avg_elevation_visible = None
            max_elevation_visible = None
            total_visible_time = 0
            avg_signal_power = None
            max_signal_power = None

        print(f"  ✓ Processed {len(positions)} data points")
        print(f"  ✓ Visible passes: {total_visible_time:.1f} minutes total")
        if max_elevation_visible:
            print(f"  ✓ Maximum elevation: {max_elevation_visible:.2f}°")

        # Create report section
        section = f"""
## {sat_name}
**NORAD ID:** {sat_info['norad_id']}
**Description:** {sat_info['description']}

### Orbital Parameters (TLE)
```
{name}
{line1}
{line2}
```

### Statistics ({start_date.strftime('%b %d')}-{end_date.strftime('%d, %Y')})
- **Total Data Points:** {len(positions):,}
- **Total Visible Time:** {total_visible_time:.1f} minutes
- **Maximum Elevation:** {max_elevation_visible:.2f}° {
    "(above horizon)" if max_elevation_visible and max_elevation_visible > 0
    else "(below horizon)"
}
- **Average Elevation (when visible):** {
    f"{avg_elevation_visible:.2f}°" if avg_elevation_visible else "N/A"
}
- **Average Signal Power (when visible):** {
    f"{avg_signal_power:.2f} dBm" if avg_signal_power else "N/A"
}
- **Peak Signal Power:** {f"{max_signal_power:.2f} dBm" if max_signal_power else "N/A"}
"""
        report_sections.append(section)

    # Generate filename suffix with date range
    date_suffix = f"{start_date.strftime('%b%d').lower()}-{end_date.strftime('%b%d').lower()}"

    # Save data to JSON
    json_filename = f"ast_satellite_data_{date_suffix}.json"
    with open(json_filename, "w") as f:
        json.dump(all_satellite_data, f, indent=2)
    print(f"\n✓ Detailed data saved to: {json_filename}")

    # Create CSV for each satellite
    for sat_name, data in all_satellite_data.items():
        csv_filename = f"ast_{sat_name.lower().replace(' ', '_')}_{date_suffix}.csv"
        df = pd.DataFrame(data["positions"])
        df.to_csv(csv_filename, index=False)
        print(f"✓ CSV data saved to: {csv_filename}")

    # Calculate analysis duration
    duration_days = (end_date - start_date).days + 1

    # Generate Markdown report
    report_content = f"""# AST SpaceMobile Satellite Report
## Trajectory and Signal Strength Analysis
### {observer_location['name']} ({observer_location['address']}) - {start_date.strftime('%B %d')}-{end_date.strftime('%d, %Y')}

---

## Executive Summary

This report provides comprehensive trajectory and signal strength analysis for all AST SpaceMobile satellites over {observer_location['name']} during the period of {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}.

**Location Details:**
- **Latitude:** {observer_location['latitude']}°N
- **Longitude:** {abs(observer_location['longitude'])}°W
- **Elevation:** {observer_location['elevation_m']} meters

**Analysis Parameters:**
- **Date Range:** {start_date.strftime('%B %d, %Y %H:%M:%S UTC')} - {end_date.strftime('%B %d, %Y %H:%M:%S UTC')}
- **Measurement Interval:** 5 seconds
- **Total Analysis Duration:** {duration_days} days
- **Satellites Analyzed:** {len(satellites)}

**AST SpaceMobile Fleet:**
AST SpaceMobile operates a constellation of satellites designed to provide direct-to-smartphone connectivity from space. The fleet includes:
- **BlueWalker 3 (BW3):** Test satellite with the largest commercial communications array in LEO
- **BlueBird Block 1 (A-E):** First generation commercial satellites (launched Sep 2024)
- **BlueBird Block 2 (FM1/BlueBird-6):** Next-generation satellite with 10x capacity (launched Dec 2025)

---

## Methodology

### Trajectory Calculation
Satellite trajectories are calculated using Two-Line Element (TLE) orbital parameters and the SGP4 propagator model. The Skyfield library is used for precise orbital mechanics calculations.

### Signal Strength Estimation
Signal strength is estimated using:
- **Free Space Path Loss (FSPL)** at ~2 GHz (cellular bands)
- **Atmospheric Attenuation** based on elevation angle
- **Link Budget Analysis** with assumed satellite EIRP of 55 dBW
- **Ground Station Gain** of 15 dBi

**Link Quality Metrics:**
- **Excellent:** SNR ≥ 20 dB
- **Good:** SNR ≥ 15 dB
- **Fair:** SNR ≥ 10 dB
- **Poor:** SNR ≥ 5 dB
- **Very Poor:** SNR < 5 dB

---

## Satellite Details

{''.join(report_sections)}

---

## Data Files

The following data files have been generated:

1. **{json_filename}** - Complete dataset in JSON format
2. **Individual CSV files** - One per satellite with 5-second interval data

### CSV Column Descriptions:
- `timestamp`: ISO 8601 formatted UTC timestamp
- `elevation_deg`: Elevation angle from observer (degrees)
- `azimuth_deg`: Azimuth angle from observer (degrees, 0°=North)
- `range_km`: Distance from observer to satellite (kilometers)
- `satellite_lat`: Satellite sub-point latitude (degrees)
- `satellite_lon`: Satellite sub-point longitude (degrees)
- `satellite_alt_km`: Satellite altitude above Earth (kilometers)
- `visible`: Boolean indicating if satellite is above horizon
- `received_power_dbm`: Estimated received signal power (dBm)
- `snr_db`: Signal-to-Noise Ratio (dB)
- `link_quality`: Qualitative link assessment
- `path_loss_db`: Total path loss (dB)
- `atmospheric_loss_db`: Atmospheric attenuation (dB)

---

## Notes and Limitations

1. **TLE Data Currency:** This analysis uses the most recent TLE data available. Orbital parameters may drift over time due to atmospheric drag and orbital maneuvers.

2. **Signal Strength Model:** The signal strength calculations are estimates based on typical LEO satcom parameters. Actual signal characteristics depend on:
   - Satellite antenna pointing
   - Transmit power and modulation
   - Atmospheric conditions
   - Interference environment
   - Ground terminal specifications

3. **Visibility:** Visibility calculations assume an unobstructed horizon. Actual visibility may be reduced by terrain, buildings, or other obstacles.

4. **Time Zone:** All timestamps are in UTC. {observer_location['name']} is in CST (UTC-6) during December.

---

## Report Generated
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
**Software:** AST SpaceMobile Satellite Analysis Library v1.0
**Data Sources:** Celestrak (TLE data), Skyfield (orbital mechanics)

---

*For questions or additional analysis, please contact the satellite operations team.*
"""

    report_filename = (
        f"AST_SpaceMobile_Satellite_Report_{start_date.strftime('%b%d')}-{end_date.strftime('%b%d-%Y')}.md"
    )
    with open(report_filename, "w") as f:
        f.write(report_content)

    print(f"\n✓ Comprehensive report saved to: {report_filename}")
    print("\n" + "=" * 80)
    print("REPORT GENERATION COMPLETE")
    print("=" * 80)

    return all_satellite_data, report_filename


def generate_pass_report(
    satellite_data_file: Optional[str] = None,
    output_dir: str = "pass_graphs",
) -> str:
    """
    Generate detailed pass analysis report with visualizations

    Args:
        satellite_data_file: Path to JSON satellite data file (auto-detected if None)
        output_dir: Directory for graph outputs

    Returns:
        Path to generated report file
    """
    import glob
    import sys

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("Loading satellite data...")

    # Look for available data files
    if satellite_data_file is None:
        data_files = glob.glob("ast_satellite_data_*.json")
        if not data_files:
            print("❌ Error: No satellite data files found.")
            print("Please run generate_trajectory_report() first to generate the data.")
            sys.exit(1)
        # Use the most recent data file
        satellite_data_file = sorted(data_files)[-1]

    print(f"Using data file: {satellite_data_file}")

    try:
        with open(satellite_data_file, "r") as f:
            satellite_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Error loading data file: {e}")
        sys.exit(1)

    print(f"Loaded data for {len(satellite_data)} satellites")

    # Determine date range from data file name
    date_range = satellite_data_file.replace("ast_satellite_data_", "").replace(".json", "")

    report_md = f"""# AST SpaceMobile Detailed Pass Analysis Report
## Signal Strength and Trajectory Analysis
### {OBSERVER_LOCATION['name']} ({OBSERVER_LOCATION['address']}) - Analysis Period: {date_range.upper()}

---

## Executive Summary

This comprehensive report provides detailed analysis of every satellite pass for all AST SpaceMobile satellites over {OBSERVER_LOCATION['name']} during the analysis period. Each pass includes:

- **Complete pass timeline** with local (CST) timestamps
- **Signal strength visualization** showing received power and SNR over time
- **Elevation profile** during each pass
- **Detailed metrics** including duration, peak signal, and link quality

**Location:** {OBSERVER_LOCATION['name']} ({OBSERVER_LOCATION['latitude']}°N, {abs(OBSERVER_LOCATION['longitude'])}°W, elevation {OBSERVER_LOCATION['elevation_m']}m)
**Time Zone:** CST (Central Standard Time, UTC-6)
**Analysis Period:** {date_range.upper()} UTC
**Data File:** {satellite_data_file}

---

## Understanding the Graphs

Each pass visualization includes two plots:

### Top Plot: Signal Power and Elevation
- **Blue solid line:** Received signal power in dBm (left y-axis)
- **Orange dashed line:** Satellite elevation angle in degrees (right y-axis)
- Higher elevation generally means stronger signal due to shorter path and less atmospheric attenuation

### Bottom Plot: Signal-to-Noise Ratio (SNR)
- **Green line:** SNR in dB
- **Horizontal reference lines:**
  - Green (20 dB): Excellent link quality
  - Yellow-green (15 dB): Good link quality
  - Yellow (10 dB): Fair link quality
  - Orange (5 dB): Poor link quality
  - Below 5 dB: Very poor link quality

---

## Pass Analysis by Satellite

"""

    # Process each satellite
    total_passes = 0
    satellite_pass_counts = {}

    for sat_name in satellite_data.keys():
        print(f"\nProcessing {sat_name}...")

        # Validate satellite data structure
        if not isinstance(satellite_data[sat_name], dict) or "positions" not in satellite_data[sat_name]:
            print(f"  ⚠️  Warning: Invalid data structure for {sat_name}, skipping")
            continue

        positions = satellite_data[sat_name]["positions"]

        if not positions:
            print(f"  ⚠️  Warning: No position data for {sat_name}, skipping")
            continue

        # Identify passes
        passes = identify_passes(positions)
        satellite_pass_counts[sat_name] = len(passes)
        total_passes += len(passes)

        print(f"  Found {len(passes)} passes")

        # Generate detailed section
        report_md += _generate_detailed_pass_section(sat_name, passes, output_dir)

    # Add summary section
    summary_section = "\n### Overall Statistics\n\n"
    summary_section += f"**Total Passes Across All Satellites:** {total_passes}\n\n"
    summary_section += "| Satellite | Number of Passes |\n"
    summary_section += "|-----------|------------------|\n"
    for sat_name, count in satellite_pass_counts.items():
        summary_section += f"| {sat_name} | {count} |\n"
    summary_section += "\n---\n"

    # Insert summary after the main header sections
    report_md = report_md.replace("## Pass Analysis by Satellite", summary_section + "## Pass Analysis by Satellite")

    # Add footer
    report_md += f"""
---

## Appendix: Methodology

### Signal Strength Calculation
The signal strength estimates are based on:
- **Frequency:** ~2 GHz (cellular bands used by AST SpaceMobile)
- **Free Space Path Loss (FSPL):** Calculated based on range and frequency
- **Atmospheric Attenuation:** Elevation-dependent losses (2-7 dB)
- **Assumed Satellite EIRP:** 55 dBW
- **Ground Station Gain:** 15 dBi

### Pass Identification
A pass is defined as a continuous period where the satellite is above the local horizon (elevation > 0°). Data is sampled at 5-second intervals throughout each pass.

### Link Quality Criteria
- **Excellent (SNR ≥ 20 dB):** Full data throughput, ideal conditions
- **Good (SNR ≥ 15 dB):** High reliability, good performance
- **Fair (SNR ≥ 10 dB):** Acceptable performance, some degradation
- **Poor (SNR ≥ 5 dB):** Marginal link, significant degradation
- **Very Poor (SNR < 5 dB):** Unreliable link, high error rate

---

## Report Metadata

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
**Analysis Tool:** AST SpaceMobile Pass Analysis Library v1.0
**Data Source:** Celestrak TLE data with SGP4 propagation
**Visualization:** Matplotlib with 5-second sampling intervals

---

*This report is for analysis purposes. Actual signal performance may vary based on satellite configuration, atmospheric conditions, and ground terminal specifications.*
"""

    # Save the report
    output_filename = "AST_SpaceMobile_Detailed_Pass_Report.md"
    with open(output_filename, "w") as f:
        f.write(report_md)

    print("\n" + "=" * 80)
    print("REPORT GENERATION COMPLETE")
    print("=" * 80)
    print(f"\n✓ Generated {total_passes} pass graphs")
    print(f"✓ Report saved to: {output_filename}")
    print(f"✓ Graphs saved to: {output_dir}/ directory")
    print("\nPass breakdown by satellite:")
    for sat_name, count in satellite_pass_counts.items():
        print(f"  - {sat_name}: {count} passes")
    print("\n" + "=" * 80)

    return output_filename


def _generate_pass_table_markdown(satellite_name: str, passes: List[List[Dict]]) -> str:
    """Generate markdown table for all passes of a satellite"""
    md = f"\n### {satellite_name} - Pass Summary\n\n"
    md += "| Pass # | Start Time (CST) | End Time (CST) | Duration | Max Elevation | Max Signal (dBm) | Avg Signal (dBm) | Peak SNR (dB) |\n"
    md += "|--------|------------------|----------------|----------|---------------|------------------|------------------|---------------|\n"

    for i, pass_data in enumerate(passes, 1):
        start_time = utc_to_cst(pass_data[0]["timestamp"])
        end_time = utc_to_cst(pass_data[-1]["timestamp"])
        duration_secs = len(pass_data) * 5

        max_elevation = max([p["elevation_deg"] for p in pass_data])
        signal_powers = [p["received_power_dbm"] for p in pass_data]
        max_signal = max(signal_powers)
        avg_signal = np.mean(signal_powers)
        snr_values = [p["snr_db"] for p in pass_data]
        peak_snr = max(snr_values)

        md += f"| {i} | {start_time.strftime('%m/%d %H:%M:%S')} | "
        md += f"{end_time.strftime('%m/%d %H:%M:%S')} | "
        md += f"{format_duration(duration_secs)} | "
        md += f"{max_elevation:.1f}° | "
        md += f"{max_signal:.1f} | "
        md += f"{avg_signal:.1f} | "
        md += f"{peak_snr:.1f} |\n"

    return md


def _generate_detailed_pass_section(satellite_name: str, passes: List[List[Dict]], output_dir: str) -> str:
    """Generate detailed section with pass tables and embedded graphs"""
    md = f"\n## {satellite_name}\n\n"
    md += f"**Total Passes Identified:** {len(passes)}\n\n"

    # Summary table
    md += _generate_pass_table_markdown(satellite_name, passes)
    md += "\n"

    # Individual pass details with graphs
    md += "\n### Detailed Pass Analysis\n\n"

    for i, pass_data in enumerate(passes, 1):
        start_time = utc_to_cst(pass_data[0]["timestamp"])
        end_time = utc_to_cst(pass_data[-1]["timestamp"])
        duration_secs = len(pass_data) * 5

        max_elevation = max([p["elevation_deg"] for p in pass_data])
        min_elevation = min([p["elevation_deg"] for p in pass_data])
        signal_powers = [p["received_power_dbm"] for p in pass_data]
        max_signal = max(signal_powers)
        min_signal = min(signal_powers)
        avg_signal = np.mean(signal_powers)

        ranges = [p["range_km"] for p in pass_data]
        min_range = min(ranges)
        max_range = max(ranges)

        snr_values = [p["snr_db"] for p in pass_data]
        peak_snr = max(snr_values)
        avg_snr = np.mean(snr_values)

        # Determine link quality at peak
        if peak_snr >= 20:
            quality = "Excellent"
        elif peak_snr >= 15:
            quality = "Good"
        elif peak_snr >= 10:
            quality = "Fair"
        elif peak_snr >= 5:
            quality = "Poor"
        else:
            quality = "Very Poor"

        md += f"\n#### Pass #{i}\n\n"
        md += f"**Time Window (CST):** {start_time.strftime('%Y-%m-%d %H:%M:%S')} to "
        md += f"{end_time.strftime('%H:%M:%S')}\n\n"

        # Create graph
        graph_filename = f"{output_dir}/{satellite_name.replace(' ', '_').lower()}_pass_{i:02d}.png"
        create_signal_strength_graph(satellite_name, i, pass_data, graph_filename)

        # Embed graph
        md += f"![{satellite_name} Pass {i}]({graph_filename})\n\n"

        # Detailed statistics table
        md += "| Metric | Value |\n"
        md += "|--------|-------|\n"
        md += f"| **Duration** | {format_duration(duration_secs)} (mm:ss) |\n"
        md += f"| **Maximum Elevation** | {max_elevation:.2f}° |\n"
        md += f"| **Minimum Elevation** | {min_elevation:.2f}° |\n"
        md += f"| **Closest Range** | {min_range:.1f} km |\n"
        md += f"| **Farthest Range** | {max_range:.1f} km |\n"
        md += f"| **Peak Signal Power** | {max_signal:.2f} dBm |\n"
        md += f"| **Minimum Signal Power** | {min_signal:.2f} dBm |\n"
        md += f"| **Average Signal Power** | {avg_signal:.2f} dBm |\n"
        md += f"| **Peak SNR** | {peak_snr:.2f} dB |\n"
        md += f"| **Average SNR** | {avg_snr:.2f} dB |\n"
        md += f"| **Link Quality at Peak** | {quality} |\n"
        md += "\n"

        # Position data table (all data points)
        md += "**Complete Position Data:**\n\n"
        md += "| Time (CST) | Elevation | Azimuth | Range (km) | Signal (dBm) | SNR (dB) |\n"
        md += "|------------|-----------|---------|------------|--------------|----------|\n"

        # Show all position data points
        for pos in pass_data:
            time = utc_to_cst(pos["timestamp"])
            md += f"| {time.strftime('%H:%M:%S')} | "
            md += f"{pos['elevation_deg']:.1f}° | "
            md += f"{pos['azimuth_deg']:.1f}° | "
            md += f"{pos['range_km']:.1f} | "
            md += f"{pos['received_power_dbm']:.1f} | "
            md += f"{pos['snr_db']:.1f} |\n"

        md += "\n---\n"

    return md
