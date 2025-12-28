"""
Pass identification and analysis
Identifies individual satellite passes from position data
"""

from typing import List, Dict


def identify_passes(positions: List[Dict]) -> List[List[Dict]]:
    """
    Identify individual satellite passes from position data
    A pass is when the satellite goes from not visible to visible and back

    Args:
        positions: List of position dictionaries with 'visible' key

    Returns:
        List of passes, where each pass is a list of position dictionaries
    """
    passes = []
    in_pass = False
    current_pass = []

    for pos in positions:
        if pos["visible"] and not in_pass:
            # Start of a new pass
            in_pass = True
            current_pass = [pos]
        elif pos["visible"] and in_pass:
            # Continue current pass
            current_pass.append(pos)
        elif not pos["visible"] and in_pass:
            # End of pass
            in_pass = False
            if len(current_pass) > 0:
                passes.append(current_pass)
            current_pass = []

    # Handle case where pass extends to end of data
    if in_pass and len(current_pass) > 0:
        passes.append(current_pass)

    return passes
