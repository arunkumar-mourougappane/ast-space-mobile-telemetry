"""
Visualization functionality for satellite passes
Creates graphs and charts for signal strength and trajectory data
"""

from datetime import datetime, timedelta
from typing import List, Dict

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def utc_to_cst(utc_time_str: str) -> datetime:
    """Convert UTC timestamp string to CST (UTC-6)"""
    utc_dt = datetime.fromisoformat(utc_time_str)
    cst_dt = utc_dt - timedelta(hours=6)
    return cst_dt


def format_duration(seconds: int) -> str:
    """Format duration in seconds to mm:ss"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def create_signal_strength_graph(
    satellite_name: str, pass_num: int, pass_data: List[Dict], output_file: str
) -> str:
    """
    Create a signal strength vs time graph for a specific pass

    Args:
        satellite_name: Name of the satellite
        pass_num: Pass number for labeling
        pass_data: List of position dictionaries for the pass
        output_file: Output file path for the graph

    Returns:
        Path to the created graph file
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
    line1 = ax1.plot(timestamps, signal_strengths, color=color1, linewidth=2, label="Signal Power")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # Add elevation on secondary y-axis
    ax1_twin = ax1.twinx()
    color2 = "tab:orange"
    ax1_twin.set_ylabel("Elevation (degrees)", color=color2, fontsize=11, fontweight="bold")
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
    labels = [line.get_label() for line in lines]
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
