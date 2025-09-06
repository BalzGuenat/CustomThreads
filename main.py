import math
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

NAME = "3D-printed Metric Threads V4"
UNIT = "mm"
ANGLE = 60.0
SIZES = list(range(1, 51))
# Standard ISO metric thread pitches for each size
# Format: {size: [coarse_pitch, fine_pitch1, fine_pitch2, ...]}
ISO_PITCHES = {
    1: [0.25, 0.2],
    2: [0.4, 0.25],
    3: [0.5, 0.35],
    4: [0.7, 0.5],
    5: [0.8, 0.5],
    6: [1.0, 0.75],
    7: [1.0],  # Less common
    8: [1.25, 1.0, 0.75],
    9: [1.25],  # Less common
    10: [1.5, 1.25, 1.0],
    11: [1.5],  # Less common
    12: [1.75, 1.5, 1.25],
    13: [1.75],  # Less common
    14: [2.0, 1.5],
    15: [2.0],  # Less common
    16: [2.0, 1.5],
    17: [2.0],  # Less common
    18: [2.5, 2.0, 1.5],
    19: [2.5],  # Less common
    20: [2.5, 2.0, 1.5],
    21: [2.5],  # Less common
    22: [2.5, 2.0, 1.5],
    23: [2.5],  # Less common
    24: [3.0, 2.0, 1.5],
    25: [3.0],  # Less common
    26: [3.0],  # Less common
    27: [3.0, 2.0, 1.5],
    28: [3.0],  # Less common
    29: [3.0],  # Less common
    30: [3.5, 2.0, 1.5],
    31: [3.5],  # Less common
    32: [3.5],  # Less common
    33: [3.5, 2.0],
    34: [3.5],  # Less common
    35: [3.5],  # Less common
    36: [4.0, 3.0],
    37: [4.0],  # Less common
    38: [4.0],  # Less common
    39: [4.0, 3.0],
    40: [4.0],  # Less common
    41: [4.0],  # Less common
    42: [4.5, 3.0],
    43: [4.5],  # Less common
    44: [4.5],  # Less common
    45: [4.5, 3.0],
    46: [4.5],  # Less common
    47: [4.5],  # Less common
    48: [5.0, 3.0],
    49: [5.0],  # Less common
    50: [5.0, 3.0]
}
OFFSETS = [.0, .1, .2, .3, .4, .5, .6, .7, .8, .9]


def designator(val: float):
    if int(val) == val:
        return str(int(val))
    else:
        return str(val)


class Thread:
    def __init__(self):
        self.gender = None
        self.clazz = None
        self.majorDia = 0
        self.pitchDia = 0
        self.minorDia = 0
        self.tapDrill = None


class ThreadProfile(ABC):
    @abstractmethod
    def sizes(self):
        pass

    @abstractmethod
    def designations(self, size):
        pass

    @abstractmethod
    def threads(self, designation):
        pass


class Metric3Dprinted(ThreadProfile):
    class Designation:
        def __init__(self, diameter, pitch):
            self.nominalDiameter = diameter
            self.pitch = pitch
            self.name = "M{}x{}".format(designator(self.nominalDiameter), designator(self.pitch))

    def __init__(self):
        self.offsets = OFFSETS

    def sizes(self):
        return SIZES

    def designations(self, size):
        # Get pitches for this size, default to [0.5] if not defined
        pitches = ISO_PITCHES.get(size, [0.5])
        return [Metric3Dprinted.Designation(size, pitch) for pitch in pitches]

    def threads(self, designation):
        ts = []
        for offset in self.offsets:
            offset_decimals = str(offset)[2:]  # skips the '0.' at the start

            # see https://en.wikipedia.org/wiki/ISO_metric_screw_thread
            P = designation.pitch
            H = 1/math.tan(math.radians(ANGLE/2)) * (P/2)
            D = designation.nominalDiameter
            Dp = D - 2 * 3*H/8
            Dmin = D - 2 * 5*H/8

            t = Thread()
            t.gender = "external"
            t.clazz = "O.{}".format(offset_decimals)
            t.majorDia = D - offset
            t.pitchDia = Dp - offset
            t.minorDia = Dmin - offset
            ts.append(t)

            t = Thread()
            t.gender = "internal"
            t.clazz = "O.{}".format(offset_decimals)
            t.majorDia = D + offset
            t.pitchDia = Dp + offset
            t.minorDia = Dmin + offset
            t.tapDrill = D - P
            ts.append(t)
        return ts


def generate():
    profile = Metric3Dprinted()

    root = ET.Element('ThreadType')
    tree = ET.ElementTree(root)

    ET.SubElement(root, "Name").text = NAME
    ET.SubElement(root, "CustomName").text = NAME
    ET.SubElement(root, "Unit").text = UNIT
    ET.SubElement(root, "Angle").text = str(ANGLE)
    ET.SubElement(root, "SortOrder").text = "3"

    for size in profile.sizes():
        thread_size_element = ET.SubElement(root, "ThreadSize")
        ET.SubElement(thread_size_element, "Size").text = str(size)
        for designation in profile.designations(size):
            designation_element = ET.SubElement(thread_size_element, "Designation")
            ET.SubElement(designation_element, "ThreadDesignation").text = designation.name
            ET.SubElement(designation_element, "CTD").text = designation.name
            ET.SubElement(designation_element, "Pitch").text = str(designation.pitch)
            for thread in profile.threads(designation):
                thread_element = ET.SubElement(designation_element, "Thread")
                ET.SubElement(thread_element, "Gender").text = thread.gender
                ET.SubElement(thread_element, "Class").text = thread.clazz
                ET.SubElement(thread_element, "MajorDia").text = "{:.4g}".format(thread.majorDia)
                ET.SubElement(thread_element, "PitchDia").text = "{:.4g}".format(thread.pitchDia)
                ET.SubElement(thread_element, "MinorDia").text = "{:.4g}".format(thread.minorDia)
                if thread.tapDrill:
                    ET.SubElement(thread_element, "TapDrill").text = "{:.4g}".format(thread.tapDrill)

    ET.indent(tree)
    tree.write('3DPrintedMetricV4.xml', encoding='UTF-8', xml_declaration=True)


generate()
