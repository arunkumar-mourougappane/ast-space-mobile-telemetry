#!/usr/bin/env python3
"""
Example: Fetch TLE data for satellites
"""

from ast_spacemobile.core.config import AST_SATELLITES
from ast_spacemobile.core.tle import fetch_tle_data

print("Fetching TLE data for AST SpaceMobile satellites...\n")

for sat_name, sat_info in AST_SATELLITES.items():
    norad_id = sat_info["norad_id"]
    print(f"{sat_name} (NORAD {norad_id}):")

    # Fetch TLE
    name, line1, line2 = fetch_tle_data(norad_id)

    if line1 and line2:
        print(f"  ✓ TLE retrieved: {name}")
        print(f"    Line 1: {line1[:30]}...")
        print(f"    Line 2: {line2[:30]}...")
    else:
        print("  ✗ Could not fetch TLE data")

    print()
