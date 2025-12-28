#!/usr/bin/env python3
"""
Example: Analyze signal strength at different elevations
"""

from ast_spacemobile.core.calculations import calculate_signal_strength

# Test signal strength at different elevation angles
elevations = [10, 20, 30, 45, 60, 75, 90]
range_km = 600  # Typical LEO satellite distance

print("Signal Strength Analysis")
print("=" * 70)
print(f"Range: {range_km} km")
print("\n{:>10} | {:>12} | {:>12} | {:>15}".format("Elevation", "Power (dBm)", "SNR (dB)", "Link Quality"))
print("-" * 70)

for elev in elevations:
    signal = calculate_signal_strength(elevation_deg=elev, range_km=range_km, azimuth_deg=0)

    print(
        f"{elev:>10}° | {signal['received_power_dbm']:>12.2f} | "
        f"{signal['snr_db']:>12.2f} | {signal['link_quality']:>15}"
    )

print("\nConclusion:")
print("- Higher elevation = stronger signal (less atmosphere to penetrate)")
print("- Excellent link quality typically at elevations > 30°")
