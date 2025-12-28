"""
AST SpaceMobile Satellite Analysis Library
A modular library for analyzing AST SpaceMobile satellite trajectories and signal strength
"""

__version__ = "1.0.0"

from ast_spacemobile.core.config import AST_SATELLITES, OBSERVER_LOCATION
from ast_spacemobile.core.tle import fetch_tle_data
from ast_spacemobile.core.calculations import (
    calculate_signal_strength,
    generate_satellite_passes,
)
from ast_spacemobile.analysis.passes import identify_passes
from ast_spacemobile.reports.generator import generate_trajectory_report, generate_pass_report

__all__ = [
    "AST_SATELLITES",
    "OBSERVER_LOCATION",
    "fetch_tle_data",
    "calculate_signal_strength",
    "generate_satellite_passes",
    "identify_passes",
    "generate_trajectory_report",
    "generate_pass_report",
]
