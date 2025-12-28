"""
TLE (Two-Line Element) data fetching functionality
Retrieves orbital parameters from Celestrak
"""

from typing import Optional, Tuple

import requests


def fetch_tle_data(norad_id: int, timeout: int = 10) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Fetch TLE data from Celestrak for a given NORAD ID

    Args:
        norad_id: NORAD catalog number for the satellite
        timeout: Request timeout in seconds

    Returns:
        Tuple of (name, line1, line2) or (None, None, None) if fetch fails
    """
    try:
        # Try Celestrak API with specific NORAD ID
        url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
        response = requests.get(url, timeout=timeout)

        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            if len(lines) >= 3:
                return lines[0].strip(), lines[1].strip(), lines[2].strip()

        # Fallback to general catalog
        url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=TLE"
        response = requests.get(url, timeout=timeout)

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


def create_simulated_tle(norad_id: int, satellite_name: str) -> Tuple[str, str, str]:
    """
    Create simulated TLE data for demonstration purposes

    Args:
        norad_id: NORAD catalog number
        satellite_name: Name of the satellite

    Returns:
        Tuple of (name, line1, line2) with simulated data
    """
    line1 = f"1 {norad_id:5d}U 22059A   25341.50000000  .00000000  00000-0  00000-0 0  9999"
    line2 = f"2 {norad_id:5d}  53.0000  95.0000 0001000  90.0000 270.0000 15.00000000000000"
    return satellite_name, line1, line2
