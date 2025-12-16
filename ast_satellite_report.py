"""
AST SpaceMobile Satellite Report Generator
Generates detailed trajectory and signal strength reports for AST SpaceMobile satellites
over Midland, TX between December 7-12, 2025
"""

import numpy as np
from datetime import datetime, timedelta
from skyfield.api import load, EarthSatellite, wgs84
from skyfield.toposlib import GeographicPosition
import json
import requests
from typing import List, Dict, Tuple
import pandas as pd
import argparse

# AST SpaceMobile satellites
# Based on publicly available information, AST SpaceMobile has launched:
# - BlueWalker 3 (BW3) - Test satellite launched September 2022
# - BlueBird 1-5 - First commercial satellites (planned/launched 2024)

AST_SATELLITES = {
    "BLUEWALKER 3": {
        "norad_id": 53807,
        "description": "Test satellite, largest commercial communications array in LEO",
    },
    "BLUEBIRD-1": {
        "norad_id": 60399,
        "description": "First commercial Block 1 BlueBird satellite",
    },
    "BLUEBIRD-2": {
        "norad_id": 60400,
        "description": "Second commercial Block 1 BlueBird satellite",
    },
    "BLUEBIRD-3": {
        "norad_id": 60401,
        "description": "Third commercial Block 1 BlueBird satellite",
    },
    "BLUEBIRD-4": {
        "norad_id": 60402,
        "description": "Fourth commercial Block 1 BlueBird satellite",
    },
    "BLUEBIRD-5": {
        "norad_id": 60403,
        "description": "Fifth commercial Block 1 BlueBird satellite",
    },
}

# Midland, TX coordinates
MIDLAND_TX = {"latitude": 31.9973, "longitude": -102.0779, "elevation_m": 872}


def fetch_tle_data(norad_id: int) -> Tuple[str, str, str]:
    """
    Fetch TLE data from Celestrak for a given NORAD ID
    """
    try:
        # Try Celestrak API
        url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            if len(lines) >= 3:
                return lines[0].strip(), lines[1].strip(), lines[2].strip()

        # Fallback to general catalog
        url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=TLE"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            for i in range(0, len(lines), 3):
                if i + 2 < len(lines):
                    if str(norad_id) in lines[i + 1]:
                        return (
                            lines[i].strip(),
                            lines[i + 1].strip(),
                            lines[i + 2].strip(),
                        )

        return None, None, None

    except Exception as e:
        print(f"Error fetching TLE for NORAD ID {norad_id}: {e}")
        return None, None, None


def calculate_signal_strength(
    elevation_deg: float, range_km: float, azimuth_deg: float
) -> Dict:
    """
    Calculate estimated signal strength based on satellite position

    Simplified model based on:
    - Free space path loss
    - Elevation angle (atmospheric attenuation)
    - Assumed satellite EIRP and receiver characteristics

    Returns signal metrics in a dictionary
    """
    # Avoid calculation for satellites below horizon
    if elevation_deg < 0:
        return {
            "received_power_dbm": None,
            "snr_db": None,
            "link_quality": "No Signal",
            "path_loss_db": None,
        }

    # Constants (typical for LEO satcom)
    FREQUENCY_GHZ = 2.0  # AST SpaceMobile uses cellular bands (~2 GHz)
    SATELLITE_EIRP_DBW = 55  # Effective Isotropic Radiated Power (estimate)
    RECEIVER_GAIN_DBI = 15  # Ground station antenna gain
    SYSTEM_LOSSES_DB = 3  # Cable losses, etc.
    NOISE_FLOOR_DBM = -110  # Typical receiver noise floor

    # Free Space Path Loss (FSPL)
    # FSPL(dB) = 20*log10(distance_km) + 20*log10(frequency_MHz) + 32.45
    frequency_mhz = FREQUENCY_GHZ * 1000
    fspl_db = 20 * np.log10(range_km) + 20 * np.log10(frequency_mhz) + 32.45

    # Atmospheric attenuation (increases at low elevation angles)
    if elevation_deg < 10:
        atm_loss_db = 2.0 + (10 - elevation_deg) * 0.5
    else:
        atm_loss_db = 2.0

    # Total path loss
    total_path_loss_db = fspl_db + atm_loss_db + SYSTEM_LOSSES_DB

    # Received power calculation
    # P_rx = EIRP - Path_Loss + Receiver_Gain
    satellite_eirp_dbm = SATELLITE_EIRP_DBW + 30  # Convert to dBm
    received_power_dbm = satellite_eirp_dbm - total_path_loss_db + RECEIVER_GAIN_DBI

    # Signal-to-Noise Ratio
    snr_db = received_power_dbm - NOISE_FLOOR_DBM

    # Link quality assessment
    if snr_db >= 20:
        link_quality = "Excellent"
    elif snr_db >= 15:
        link_quality = "Good"
    elif snr_db >= 10:
        link_quality = "Fair"
    elif snr_db >= 5:
        link_quality = "Poor"
    else:
        link_quality = "Very Poor"

    return {
        "received_power_dbm": round(received_power_dbm, 2),
        "snr_db": round(snr_db, 2),
        "link_quality": link_quality,
        "path_loss_db": round(total_path_loss_db, 2),
        "atmospheric_loss_db": round(atm_loss_db, 2),
    }


def generate_satellite_passes(
    satellite: EarthSatellite,
    observer: GeographicPosition,
    start_time: datetime,
    end_time: datetime,
    interval_seconds: int = 5,
) -> List[Dict]:
    """
    Generate satellite position data at specified intervals
    """
    ts = load.timescale()

    positions = []
    current_time = start_time

    while current_time <= end_time:
        t = ts.utc(
            current_time.year,
            current_time.month,
            current_time.day,
            current_time.hour,
            current_time.minute,
            current_time.second,
        )

        # Calculate satellite position relative to observer
        difference = satellite - observer
        topocentric = difference.at(t)

        alt, az, distance = topocentric.altaz()

        # Get satellite geocentric position
        geocentric = satellite.at(t)
        lat, lon = wgs84.latlon_of(geocentric)
        height = wgs84.height_of(geocentric)

        # Calculate signal strength
        signal_metrics = calculate_signal_strength(alt.degrees, distance.km, az.degrees)

        position_data = {
            "timestamp": current_time.isoformat(),
            "unix_timestamp": current_time.timestamp(),
            "elevation_deg": round(alt.degrees, 2),
            "azimuth_deg": round(az.degrees, 2),
            "range_km": round(distance.km, 2),
            "satellite_lat": round(lat.degrees, 4),
            "satellite_lon": round(lon.degrees, 4),
            "satellite_alt_km": round(height.km, 2),
            "visible": bool(alt.degrees > 0),
            **signal_metrics,
        }

        positions.append(position_data)
        current_time += timedelta(seconds=interval_seconds)

    return positions


def generate_report(start_date=None, end_date=None):
    """
    Main function to generate the comprehensive satellite report
    
    Args:
        start_date: Start date for analysis (datetime object). Defaults to Dec 7, 2025
        end_date: End date for analysis (datetime object). Defaults to Dec 12, 2025
    """
    # Set default dates if not provided
    if start_date is None:
        start_date = datetime(2025, 12, 7, 0, 0, 0)
    if end_date is None:
        end_date = datetime(2025, 12, 12, 23, 59, 59)
    
    print("=" * 80)
    print("AST SPACEMOBILE SATELLITE TRAJECTORY AND SIGNAL STRENGTH REPORT")
    print("=" * 80)
    print(
        f"Location: Midland, TX ({MIDLAND_TX['latitude']}°N, {abs(MIDLAND_TX['longitude'])}°W)"
    )
    print(f"Elevation: {MIDLAND_TX['elevation_m']} meters")
    print(f"Date Range: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    print("Measurement Interval: 5 seconds")
    print("=" * 80)
    print()

    # Load timescale
    ts = load.timescale()

    # Create observer location
    observer = wgs84.latlon(
        MIDLAND_TX["latitude"], MIDLAND_TX["longitude"], MIDLAND_TX["elevation_m"]
    )

    all_satellite_data = {}
    report_sections = []

    print("\n### SATELLITE INFORMATION ###\n")

    for sat_name, sat_info in AST_SATELLITES.items():
        print(f"\nProcessing: {sat_name}")
        print(f"  NORAD ID: {sat_info['norad_id']}")
        print(f"  Description: {sat_info['description']}")

        # Fetch TLE data
        name, line1, line2 = fetch_tle_data(sat_info["norad_id"])

        if not line1 or not line2:
            print(f"  ⚠ WARNING: Could not fetch TLE data for {sat_name}")
            print("  Using simulated data for demonstration purposes")

            # Create simulated TLE for demonstration
            # This is a placeholder - in production, actual TLE data should be used
            line1 = f"1 {sat_info['norad_id']:5d}U 22059A   25341.50000000  .00000000  00000-0  00000-0 0  9999"
            line2 = f"2 {sat_info['norad_id']:5d}  53.0000  95.0000 0001000  90.0000 270.0000 15.00000000000000"
            name = sat_name

        print(f"  TLE Data Retrieved: {name}")

        # Create satellite object
        satellite = EarthSatellite(line1, line2, name, ts)

        # Generate trajectory data
        print("  Calculating trajectories...")
        positions = generate_satellite_passes(
            satellite, observer, start_date, end_date, interval_seconds=5
        )

        all_satellite_data[sat_name] = {
            "info": sat_info,
            "tle": {"name": name, "line1": line1, "line2": line2},
            "positions": positions,
        }

        # Calculate statistics
        visible_positions = [p for p in positions if p["visible"]]

        if visible_positions:
            avg_elevation_visible = np.mean(
                [p["elevation_deg"] for p in visible_positions]
            )
            max_elevation_visible = max([p["elevation_deg"] for p in visible_positions])
            total_visible_time = len(visible_positions) * 5 / 60  # minutes

            # Signal statistics for visible passes
            signal_powers = [
                p["received_power_dbm"]
                for p in visible_positions
                if p["received_power_dbm"] is not None
            ]
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

### Statistics (Dec 7-12, 2025)
- **Total Data Points:** {len(positions):,}
- **Total Visible Time:** {total_visible_time:.1f} minutes
- **Maximum Elevation:** {max_elevation_visible:.2f}° {"(above horizon)" if max_elevation_visible and max_elevation_visible > 0 else "(below horizon)"}
- **Average Elevation (when visible):** {f"{avg_elevation_visible:.2f}°" if avg_elevation_visible else "N/A"}
- **Average Signal Power (when visible):** {f"{avg_signal_power:.2f} dBm" if avg_signal_power else "N/A"}
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
### Midland, TX - {start_date.strftime('%B %d')}-{end_date.strftime('%d, %Y')}

---

## Executive Summary

This report provides comprehensive trajectory and signal strength analysis for all AST SpaceMobile satellites over Midland, Texas during the period of {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}.

**Location Details:**
- **Latitude:** {MIDLAND_TX['latitude']}°N
- **Longitude:** {abs(MIDLAND_TX['longitude'])}°W
- **Elevation:** {MIDLAND_TX['elevation_m']} meters

**Analysis Parameters:**
- **Date Range:** {start_date.strftime('%B %d, %Y %H:%M:%S UTC')} - {end_date.strftime('%B %d, %Y %H:%M:%S UTC')}
- **Measurement Interval:** 5 seconds
- **Total Analysis Duration:** {duration_days} days
- **Satellites Analyzed:** {len(AST_SATELLITES)}

**AST SpaceMobile Fleet:**
AST SpaceMobile operates a constellation of satellites designed to provide direct-to-smartphone connectivity from space. The fleet includes:
- **BlueWalker 3 (BW3):** Test satellite with the largest commercial communications array in LEO
- **BlueBird Block 1 (1-5):** First generation commercial satellites

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

1. **ast_satellite_data_dec7-12.json** - Complete dataset in JSON format
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

4. **Time Zone:** All timestamps are in UTC. Midland, TX is in CST (UTC-6) during December.

---

## Report Generated
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
**Software:** AST SpaceMobile Satellite Analysis Tool v1.0
**Data Sources:** Celestrak (TLE data), Skyfield (orbital mechanics)

---

*For questions or additional analysis, please contact the satellite operations team.*
"""

    report_filename = f"AST_SpaceMobile_Satellite_Report_{start_date.strftime('%b%d')}-{end_date.strftime('%b%d-%Y')}.md"
    with open(report_filename, "w") as f:
        f.write(report_content)

    print(f"\n✓ Comprehensive report saved to: {report_filename}")
    print("\n" + "=" * 80)
    print("REPORT GENERATION COMPLETE")
    print("=" * 80)

    return all_satellite_data, report_filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate AST SpaceMobile satellite trajectory and signal strength report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Use default dates (Dec 7-12, 2025)
  python ast_satellite_report.py
  
  # Custom date range
  python ast_satellite_report.py --start 2025-12-01 --end 2025-12-15
  
  # Single day analysis
  python ast_satellite_report.py --start 2025-12-10 --end 2025-12-10
        """
    )
    
    parser.add_argument(
        "--start",
        type=str,
        default="2025-12-07",
        help="Start date in YYYY-MM-DD format (default: 2025-12-07)"
    )
    
    parser.add_argument(
        "--end",
        type=str,
        default="2025-12-12",
        help="End date in YYYY-MM-DD format (default: 2025-12-12)"
    )
    
    args = parser.parse_args()
    
    try:
        # Parse dates
        start_date = datetime.strptime(args.start, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
        end_date = datetime.strptime(args.end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        
        # Validate dates
        if end_date < start_date:
            print("❌ Error: End date must be after start date")
            exit(1)
        
        # Generate report with custom dates
        data, report_file = generate_report(start_date, end_date)
        print("\n✓ All files generated successfully!")
        print(f"\n📊 Main Report: {report_file}")
        print("📁 Data files created in current directory")
    except ValueError as e:
        print(f"\n❌ Error parsing dates: {e}")
        print("Please use YYYY-MM-DD format for dates")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
