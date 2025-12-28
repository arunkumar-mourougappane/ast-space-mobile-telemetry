#!/usr/bin/env python3
"""
Example: Generate report for a custom observer location
"""

from datetime import datetime

from ast_spacemobile import generate_trajectory_report

# Define a custom observer location (New York City)
nyc_location = {
    "name": "New York City",
    "address": "Times Square",
    "latitude": 40.7580,
    "longitude": -73.9855,
    "elevation_m": 10,
}

# Generate report for NYC
start_date = datetime(2025, 12, 7)
end_date = datetime(2025, 12, 8)

print(f"Generating report for {nyc_location['name']}...")
satellite_data, report_file = generate_trajectory_report(
    start_date=start_date, end_date=end_date, observer_location=nyc_location
)

print(f"\n✓ Report generated: {report_file}")
print(f"✓ Location: {nyc_location['name']} ({nyc_location['latitude']}°N, "
      f"{abs(nyc_location['longitude'])}°W)")
