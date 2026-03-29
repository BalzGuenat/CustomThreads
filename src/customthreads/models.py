"""Thread profile and generator models."""

import math
from abc import ABC, abstractmethod
from .utils import format_number


class Thread:
    """Represents a single thread with calculated dimensions."""
    
    def __init__(self):
        self.gender = None
        self.clazz = None
        self.majorDia = 0
        self.pitchDia = 0
        self.minorDia = 0
        self.tapDrill = None


class ThreadProfile(ABC):
    """Abstract base class for thread profiles."""
    
    @abstractmethod
    def sizes(self):
        """Return list of available thread sizes."""
        pass

    @abstractmethod
    def designations(self, size):
        """Return designations for a given size."""
        pass

    @abstractmethod
    def threads(self, designation):
        """Return threads for a given designation."""
        pass


class MetricThreadGenerator(ThreadProfile):
    """Generator for metric 3D-printed threads."""
    
    class Designation:
        """Represents a thread designation (e.g., M8x1)."""
        
        def __init__(self, diameter, pitch):
            self.nominalDiameter = diameter
            self.pitch = pitch
            self.name = f"M{format_number(diameter)}x{format_number(pitch)}"

    def __init__(self, pitch_list, thread_sizes, tolerance_offsets, thread_angle):
        """Initialize generator with configuration.
        
        Args:
            pitch_list: List of pitch values to generate
            thread_sizes: List of thread diameters to generate
            tolerance_offsets: List of tolerance offsets for thread classes
            thread_angle: Thread angle in degrees (typically 60.0)
        """
        self.pitches = pitch_list
        self.thread_sizes = thread_sizes
        self.tolerance_offsets = tolerance_offsets
        self.thread_angle = thread_angle

    def sizes(self):
        """Return available thread sizes."""
        return self.thread_sizes

    def designations(self, size):
        """Return designations for a given size."""
        return [self.Designation(size, pitch) for pitch in self.pitches]

    def threads(self, designation):
        """Generate threads for a designation with all tolerance classes."""
        ts = []
        for offset in self.tolerance_offsets:
            offset_decimals = str(offset)[2:]  # skips the '0.' at the start

            # see https://en.wikipedia.org/wiki/ISO_metric_screw_thread
            P = designation.pitch
            H = 1 / math.tan(math.radians(self.thread_angle / 2)) * (P / 2)
            D = designation.nominalDiameter
            Dp = D - 2 * 3 * H / 8
            Dmin = D - 2 * 5 * H / 8

            t = Thread()
            t.gender = "external"
            t.clazz = f"O.{offset_decimals}"
            t.majorDia = D - offset
            t.pitchDia = Dp - offset
            t.minorDia = Dmin - offset
            ts.append(t)

            t = Thread()
            t.gender = "internal"
            t.clazz = f"O.{offset_decimals}"
            t.majorDia = D + offset
            t.pitchDia = Dp + offset
            t.minorDia = Dmin + offset
            t.tapDrill = D - P
            ts.append(t)
        return ts
