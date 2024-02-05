import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

NAME = "3D-printed Metric Threads"
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
    class Desig:
        def __init__(self, size, pitch):
            self.size = size
            self.pitch = pitch
            self.name = "M{}x{}".format(designator(self.size), designator(self.pitch))

        def depth(self):
            return self.pitch

    def __init__(self):
        self.offsets = OFFSETS

    def sizes(self):
        return SIZES

    def designations(self, size):
        return [Metric3Dprinted.Desig(size, pitch) for pitch in PITCHES]

    def threads(self, designation):
        ts = []
        for offset in self.offsets:
            offset_decimals = str(offset)[2:]  # skips the '0.' at the start
            depth = designation.depth()
            # the tolerances below are based on ISO M30x3.5 6g/6H
            t = Thread()
            t.gender = "external"
            t.clazz = "O.{}".format(offset_decimals)
            t.majorDia = designation.size - offset
            t.pitchDia = designation.size - offset - depth / 4
            t.minorDia = designation.size - offset - depth / 2
            ts.append(t)

            t = Thread()
            t.gender = "internal"
            t.clazz = "O.{}".format(offset_decimals)
            t.majorDia = designation.size + offset
            t.pitchDia = designation.size + offset - depth / 4
            t.minorDia = designation.size + offset - depth / 2
            ts.append(t)
        return ts


profile = Metric3Dprinted()


root = ET.Element('ThreadType')
tree = ET.ElementTree(root)

ET.SubElement(root, "Name").text = NAME
ET.SubElement(root, "CustomName").text = NAME
ET.SubElement(root, "Unit").text = UNIT
ET.SubElement(root, "Angle").text = str(ANGLE)
ET.SubElement(root, "SortOrder").text = "3"


for size in profile.sizes():
    ts = ET.SubElement(root, "ThreadSize")
    ET.SubElement(ts, "Size").text = str(size)
    for des in profile.designations(size):
        deselem = ET.SubElement(ts, "Designation")
        ET.SubElement(deselem, "ThreadDesignation").text = des.name
        ET.SubElement(deselem, "CTD").text = des.name
        ET.SubElement(deselem, "Pitch").text = str(des.pitch)
        for t in profile.threads(des):
            elem = ET.SubElement(deselem, "Thread")
            ET.SubElement(elem, "Gender").text = t.gender
            ET.SubElement(elem, "Class").text = t.clazz
            ET.SubElement(elem, "MajorDia").text = "{:.4g}".format(t.majorDia)
            ET.SubElement(elem, "PitchDia").text = "{:.4g}".format(t.pitchDia)
            ET.SubElement(elem, "MinorDia").text = "{:.4g}".format(t.minorDia)
            if t.tapDrill:
                ET.SubElement(elem, "TapDrill").text = "{:.4g}".format(t.tapDrill)

ET.indent(tree)
tree.write('output.xml', encoding='UTF-8', xml_declaration=True)
