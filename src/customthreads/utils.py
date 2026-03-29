"""Shared utility helpers for the customthreads package."""


def format_number(val):
    """Format numbers for display (e.g., 5.0 -> "5")."""
    return str(int(val)) if val == int(val) else str(val)
