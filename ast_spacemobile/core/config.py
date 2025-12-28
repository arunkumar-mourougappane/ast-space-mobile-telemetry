"""
Configuration for AST SpaceMobile satellite tracking
Contains satellite catalog and observer location data
"""

# AST SpaceMobile satellites
# Based on publicly available information, AST SpaceMobile has launched:
# - BlueWalker 3 (BW3) - Test satellite launched September 2022
# - BlueBird A-E (Block 1) - First commercial satellites launched September 2024
# - BlueBird 6 (Block 2) - Next-gen satellite launched December 2025

AST_SATELLITES = {
    "BLUEWALKER 3": {
        "norad_id": 53807,
        "description": "Test satellite, largest commercial communications array in LEO",
    },
    "BLUEBIRD-A": {
        "norad_id": 61045,
        "description": "Block 1 BlueBird satellite (SPACEMOBILE-003), launched Sep 2024",
    },
    "BLUEBIRD-B": {
        "norad_id": 61046,
        "description": "Block 1 BlueBird satellite (SPACEMOBILE-005), launched Sep 2024",
    },
    "BLUEBIRD-C": {
        "norad_id": 61047,
        "description": "Block 1 BlueBird satellite (SPACEMOBILE-001), launched Sep 2024",
    },
    "BLUEBIRD-D": {
        "norad_id": 61048,
        "description": "Block 1 BlueBird satellite (SPACEMOBILE-002), launched Sep 2024",
    },
    "BLUEBIRD-E": {
        "norad_id": 61049,
        "description": "Block 1 BlueBird satellite (SPACEMOBILE-004), launched Sep 2024",
    },
    "BLUEBIRD-6": {
        "norad_id": 67232,
        "description": "Block 2 BlueBird satellite (FM1), launched Dec 2025, 10x capacity of Block 1",
    },
}

# Default observer location: Odessa, TX (1 Fairway Dr, Odessa, TX 79765)
OBSERVER_LOCATION = {
    "name": "Odessa, TX",
    "address": "1 Fairway Dr, Odessa, TX 79765",
    "latitude": 31.8457,
    "longitude": -102.3676,
    "elevation_m": 895,
}

# Signal calculation constants (typical for LEO satcom)
SIGNAL_PARAMS = {
    "frequency_ghz": 2.0,  # AST SpaceMobile uses cellular bands (~2 GHz)
    "satellite_eirp_dbw": 55,  # Effective Isotropic Radiated Power (estimate)
    "receiver_gain_dbi": 15,  # Ground station antenna gain
    "system_losses_db": 3,  # Cable losses, etc.
    "noise_floor_dbm": -110,  # Typical receiver noise floor
}

# Link quality thresholds (SNR in dB)
LINK_QUALITY_THRESHOLDS = {
    "excellent": 20,
    "good": 15,
    "fair": 10,
    "poor": 5,
}
