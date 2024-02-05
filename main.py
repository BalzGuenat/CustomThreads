import math
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

NAME = "3D-printed Metric Threads V2"
UNIT = "mm"
ANGLE = 60.0
SIZES = list(range(8, 51))
PITCHES = [3.5, 5.0]
OFFSETS = [.0, .1, .2, .4, .8]


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
        return [Metric3Dprinted.Designation(size, pitch) for pitch in PITCHES]

    def threads(self, designation):
        ts = []
        for offset in self.offsets:
            offset_decimals = str(offset)[2:]  # skips the '0.' at the start

            # see https://en.wikipedia.org/wiki/ISO_metric_screw_thread
            P = designation.pitch
            H = 1/math.tan(math.radians(ANGLE/2)) * (P/2)
            D = designation.nominalDiameter
            Dp = D - H/2
            Dmin = D - 5*H/8

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
    tree.write('output.xml', encoding='UTF-8', xml_declaration=True)


generate()
