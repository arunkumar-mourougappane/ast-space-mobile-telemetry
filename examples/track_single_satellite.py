#!/usr/bin/env python3
"""
Example: Track a single satellite (BlueBird-6)
"""

from datetime import datetime

from ast_spacemobile import generate_trajectory_report

# Track only BlueBird-6 (the newest Block 2 satellite)
bluebird_6_only = {
    "BLUEBIRD-6": {
        "norad_id": 67232,
        "description": "Block 2 BlueBird satellite (FM1), launched Dec 2025, 10x capacity of Block 1",
    },
}

# Generate report for one week
start_date = datetime(2025, 12, 7)
end_date = datetime(2025, 12, 14)

print("Tracking BlueBird-6 only...")
satellite_data, report_file = generate_trajectory_report(
    start_date=start_date, end_date=end_date, satellites=bluebird_6_only
)

print(f"\n✓ Report generated: {report_file}")

# Analyze the data
bb6_data = satellite_data["BLUEBIRD-6"]
positions = bb6_data["positions"]
visible_positions = [p for p in positions if p["visible"]]

if visible_positions:
    total_visible_time = len(visible_positions) * 5 / 60  # minutes
    max_elevation = max(p["elevation_deg"] for p in visible_positions)
    max_signal = max(p["received_power_dbm"] for p in visible_positions if p["received_power_dbm"])

    print("\nBlueBird-6 Statistics:")
    print(f"  - Total visible time: {total_visible_time:.1f} minutes")
    print(f"  - Maximum elevation: {max_elevation:.1f}°")
    print(f"  - Peak signal power: {max_signal:.1f} dBm")
    print(f"  - Total data points: {len(positions):,}")
