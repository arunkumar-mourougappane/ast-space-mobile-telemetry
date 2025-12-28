#!/usr/bin/env python3
"""
Basic example: Generate a trajectory report for AST SpaceMobile satellites
"""

from datetime import datetime

from ast_spacemobile import generate_trajectory_report

# Generate trajectory report for a single day
start_date = datetime(2025, 12, 7)
end_date = datetime(2025, 12, 7, 23, 59, 59)

print("Generating trajectory report...")
satellite_data, report_file = generate_trajectory_report(start_date, end_date)

print(f"\n✓ Report generated: {report_file}")
print(f"✓ Tracked {len(satellite_data)} satellites")

# Show statistics for each satellite
for sat_name, data in satellite_data.items():
    positions = data["positions"]
    visible = [p for p in positions if p["visible"]]
    if visible:
        max_elev = max(p["elevation_deg"] for p in visible)
        print(f"\n{sat_name}:")
        print(f"  - Visible time: {len(visible) * 5 / 60:.1f} minutes")
        print(f"  - Max elevation: {max_elev:.1f}°")
