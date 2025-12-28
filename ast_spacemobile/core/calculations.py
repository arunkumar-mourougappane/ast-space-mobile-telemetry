"""
Satellite trajectory and signal strength calculations
Uses Skyfield for orbital mechanics and calculates link budgets
"""

from datetime import datetime, timedelta
from typing import Dict, List

import numpy as np
from skyfield.api import EarthSatellite, wgs84
from skyfield.toposlib import GeographicPosition

from ast_spacemobile.core.config import LINK_QUALITY_THRESHOLDS, SIGNAL_PARAMS


def calculate_signal_strength(elevation_deg: float, range_km: float, azimuth_deg: float) -> Dict:
    """
    Calculate estimated signal strength based on satellite position

    Simplified model based on:
    - Free space path loss
    - Elevation angle (atmospheric attenuation)
    - Assumed satellite EIRP and receiver characteristics

    Args:
        elevation_deg: Elevation angle from observer (degrees)
        range_km: Distance from observer to satellite (kilometers)
        azimuth_deg: Azimuth angle from observer (degrees, 0°=North)

    Returns:
        Dictionary with signal metrics (received_power_dbm, snr_db, link_quality, etc.)
    """
    # Avoid calculation for satellites below horizon
    if elevation_deg < 0:
        return {
            "received_power_dbm": None,
            "snr_db": None,
            "link_quality": "No Signal",
            "path_loss_db": None,
            "atmospheric_loss_db": None,
        }

    # Get signal parameters
    frequency_ghz = SIGNAL_PARAMS["frequency_ghz"]
    satellite_eirp_dbw = SIGNAL_PARAMS["satellite_eirp_dbw"]
    receiver_gain_dbi = SIGNAL_PARAMS["receiver_gain_dbi"]
    system_losses_db = SIGNAL_PARAMS["system_losses_db"]
    noise_floor_dbm = SIGNAL_PARAMS["noise_floor_dbm"]

    # Free Space Path Loss (FSPL)
    # FSPL(dB) = 20*log10(distance_km) + 20*log10(frequency_MHz) + 32.45
    frequency_mhz = frequency_ghz * 1000
    fspl_db = 20 * np.log10(range_km) + 20 * np.log10(frequency_mhz) + 32.45

    # Atmospheric attenuation (increases at low elevation angles)
    if elevation_deg < 10:
        atm_loss_db = 2.0 + (10 - elevation_deg) * 0.5
    else:
        atm_loss_db = 2.0

    # Total path loss
    total_path_loss_db = fspl_db + atm_loss_db + system_losses_db

    # Received power calculation
    # P_rx = EIRP - Path_Loss + Receiver_Gain
    satellite_eirp_dbm = satellite_eirp_dbw + 30  # Convert to dBm
    received_power_dbm = satellite_eirp_dbm - total_path_loss_db + receiver_gain_dbi

    # Signal-to-Noise Ratio
    snr_db = received_power_dbm - noise_floor_dbm

    # Link quality assessment
    thresholds = LINK_QUALITY_THRESHOLDS
    if snr_db >= thresholds["excellent"]:
        link_quality = "Excellent"
    elif snr_db >= thresholds["good"]:
        link_quality = "Good"
    elif snr_db >= thresholds["fair"]:
        link_quality = "Fair"
    elif snr_db >= thresholds["poor"]:
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

    Args:
        satellite: Skyfield EarthSatellite object
        observer: Observer geographic position
        start_time: Start time for trajectory calculation
        end_time: End time for trajectory calculation
        interval_seconds: Time interval between calculations (default: 5 seconds)

    Returns:
        List of position dictionaries with timestamp, elevation, azimuth, range, and signal data
    """
    from skyfield.api import load

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
