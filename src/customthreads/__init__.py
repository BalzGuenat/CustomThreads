"""3D-Printed Metric Threads Generator - Core package."""

from .models import Thread, ThreadProfile, MetricThreadGenerator
from .generator import generate_pitch_list, generate_xml
from .utils import format_number

__version__ = "1.0.0"
__all__ = [
    "Thread",
    "ThreadProfile", 
    "MetricThreadGenerator",
    "generate_pitch_list",
    "format_number",
    "generate_xml",
]
