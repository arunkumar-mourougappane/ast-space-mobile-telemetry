"""
AST SpaceMobile Pass Analysis and Visualization
Creates detailed markdown report with pass tables and signal strength graphs
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import os

# Create output directories
os.makedirs("pass_graphs", exist_ok=True)

# Load the satellite data
print("Loading satellite data...")
with open("ast_satellite_data_dec7-12.json", "r") as f:
    satellite_data = json.load(f)

print(f"Loaded data for {len(satellite_data)} satellites")


def identify_passes(positions):
    """
    Identify individual satellite passes from position data
    A pass is when the satellite goes from not visible to visible and back
    """
    passes = []
    in_pass = False
    current_pass = []

    for i, pos in enumerate(positions):
        if pos["visible"] and not in_pass:
            # Start of a new pass
            in_pass = True
            current_pass = [pos]
        elif pos["visible"] and in_pass:
            # Continue current pass
            current_pass.append(pos)
        elif not pos["visible"] and in_pass:
            # End of pass
            in_pass = False
            if len(current_pass) > 0:
                passes.append(current_pass)
            current_pass = []

    # Handle case where pass extends to end of data
    if in_pass and len(current_pass) > 0:
        passes.append(current_pass)

    return passes


def utc_to_cst(utc_time_str):
    """Convert UTC timestamp to CST (UTC-6)"""
    utc_dt = datetime.fromisoformat(utc_time_str)
    cst_dt = utc_dt - timedelta(hours=6)
    return cst_dt


def format_duration(seconds):
    """Format duration in seconds to mm:ss"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def create_signal_strength_graph(satellite_name, pass_num, pass_data, output_file):
    """
    Create a signal strength vs time graph for a specific pass
    """
    # Extract timestamps and signal strengths
    timestamps = [utc_to_cst(pos["timestamp"]) for pos in pass_data]
    signal_strengths = [pos["received_power_dbm"] for pos in pass_data]
    elevations = [pos["elevation_deg"] for pos in pass_data]
    snr_values = [pos["snr_db"] for pos in pass_data]

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot 1: Signal Strength
    color1 = "tab:blue"
    ax1.set_ylabel("Received Power (dBm)", color=color1, fontsize=11, fontweight="bold")
    line1 = ax1.plot(
        timestamps, signal_strengths, color=color1, linewidth=2, label="Signal Power"
    )
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # Add elevation on secondary y-axis
    ax1_twin = ax1.twinx()
    color2 = "tab:orange"
    ax1_twin.set_ylabel(
        "Elevation (degrees)", color=color2, fontsize=11, fontweight="bold"
    )
    line2 = ax1_twin.plot(
        timestamps,
        elevations,
        color=color2,
        linewidth=2,
        linestyle="--",
        alpha=0.7,
        label="Elevation",
    )
    ax1_twin.tick_params(axis="y", labelcolor=color2)

    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", fontsize=9)

    # Plot 2: SNR
    color3 = "tab:green"
    ax2.set_ylabel("SNR (dB)", color=color3, fontsize=11, fontweight="bold")
    ax2.plot(timestamps, snr_values, color=color3, linewidth=2)
    ax2.tick_params(axis="y", labelcolor=color3)
    ax2.grid(True, alpha=0.3)

    # Add SNR quality threshold lines
    ax2.axhline(y=20, color="green", linestyle=":", alpha=0.5, label="Excellent")
    ax2.axhline(y=15, color="yellowgreen", linestyle=":", alpha=0.5, label="Good")
    ax2.axhline(y=10, color="yellow", linestyle=":", alpha=0.5, label="Fair")
    ax2.axhline(y=5, color="orange", linestyle=":", alpha=0.5, label="Poor")
    ax2.legend(loc="upper left", fontsize=8)

    # Format x-axis
    ax2.set_xlabel("Time (CST)", fontsize=11, fontweight="bold")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    plt.xticks(rotation=45, ha="right")

    # Title
    start_time = timestamps[0].strftime("%Y-%m-%d %H:%M CST")
    max_elev = max(elevations)
    duration_secs = len(pass_data) * 5

    fig.suptitle(
        f"{satellite_name} - Pass #{pass_num}\n"
        f"Start: {start_time} | Duration: {format_duration(duration_secs)} | "
        f"Max Elevation: {max_elev:.1f}°",
        fontsize=13,
        fontweight="bold",
    )

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close()

    return output_file


def generate_pass_table_markdown(satellite_name, passes):
    """
    Generate markdown table for all passes of a satellite
    """
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


def generate_detailed_pass_section(satellite_name, passes):
    """
    Generate detailed section with pass tables and embedded graphs
    """
    md = f"\n## {satellite_name}\n\n"
    md += f"**Total Passes Identified:** {len(passes)}\n\n"

    # Summary table
    md += generate_pass_table_markdown(satellite_name, passes)
    md += "\n"

    # Individual pass details with graphs
    md += f"\n### Detailed Pass Analysis\n\n"

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
        graph_filename = (
            f"pass_graphs/{satellite_name.replace(' ', '_').lower()}_pass_{i:02d}.png"
        )
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


# Main report generation
print("\nAnalyzing satellite passes...")

report_md = """# AST SpaceMobile Detailed Pass Analysis Report
## Signal Strength and Trajectory Analysis
### Midland, TX - December 7-12, 2025

---

## Executive Summary

This comprehensive report provides detailed analysis of every satellite pass for all AST SpaceMobile satellites over Midland, Texas during December 7-12, 2025. Each pass includes:

- **Complete pass timeline** with local (CST) timestamps
- **Signal strength visualization** showing received power and SNR over time
- **Elevation profile** during each pass
- **Detailed metrics** including duration, peak signal, and link quality

**Location:** Midland, TX (31.9973°N, 102.0779°W, elevation 872m)  
**Time Zone:** CST (Central Standard Time, UTC-6)  
**Analysis Period:** December 7, 2025 00:00 UTC to December 12, 2025 23:59 UTC

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
    positions = satellite_data[sat_name]["positions"]

    # Identify passes
    passes = identify_passes(positions)
    satellite_pass_counts[sat_name] = len(passes)
    total_passes += len(passes)

    print(f"  Found {len(passes)} passes")

    # Generate detailed section
    report_md += generate_detailed_pass_section(sat_name, passes)

# Add summary section at the beginning
summary_section = f"\n### Overall Statistics\n\n"
summary_section += f"**Total Passes Across All Satellites:** {total_passes}\n\n"
summary_section += "| Satellite | Number of Passes |\n"
summary_section += "|-----------|------------------|\n"
for sat_name, count in satellite_pass_counts.items():
    summary_section += f"| {sat_name} | {count} |\n"
summary_section += "\n---\n"

# Insert summary after the main header sections
report_md = report_md.replace(
    "## Pass Analysis by Satellite", summary_section + "## Pass Analysis by Satellite"
)

# Add footer
report_md += (
    """
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

**Generated:** """
    + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    + """  
**Analysis Tool:** AST SpaceMobile Pass Analysis v1.0  
**Data Source:** Celestrak TLE data with SGP4 propagation  
**Visualization:** Matplotlib with 5-second sampling intervals

---

*This report is for analysis purposes. Actual signal performance may vary based on satellite configuration, atmospheric conditions, and ground terminal specifications.*
"""
)

# Save the report
output_filename = "AST_SpaceMobile_Detailed_Pass_Report.md"
with open(output_filename, "w") as f:
    f.write(report_md)

print(f"\n{'='*80}")
print(f"REPORT GENERATION COMPLETE")
print(f"{'='*80}")
print(f"\n✓ Generated {total_passes} pass graphs")
print(f"✓ Report saved to: {output_filename}")
print(f"✓ Graphs saved to: pass_graphs/ directory")
print(f"\nPass breakdown by satellite:")
for sat_name, count in satellite_pass_counts.items():
    print(f"  - {sat_name}: {count} passes")
print(f"\n{'='*80}")
