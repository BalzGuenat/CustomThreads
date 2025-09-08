# ============================================================
# 🚀 USER INPUT SECTION — START HERE
# Change the values below to customize your thread generation
# ============================================================

# 🔧 Pitch range settings (in millimeters)
pitch_start = 1.0     # Starting pitch value (e.g., 1.0 mm)
pitch_end = 6.0       # Ending pitch value (e.g., 6.0 mm)
pitch_step = 0.5      # Interval between pitches (e.g., 0.5 mm)

# 📏 Thread diameters to include (in millimeters)
thread_sizes = list(range(8, 51))  # Diameters from 8 mm to 50 mm

# ⚙️ Tolerance offsets to simulate different thread classes
tolerance_offsets = [0.0, 0.1, 0.2, 0.4, 0.8]

# 🧾 Output file name
output_filename = "3DPrintedMetricThreads.xml"

# 📋 Metadata for the thread type
thread_name = "3D-Printed Metric Threads V3"
unit = "mm"
thread_angle = 60.0  # Standard ISO metric thread angle

# ============================================================
# 🚫 USER INPUT SECTION — END HERE
# You don't need to change anything below this line
# ============================================================

import math
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

# 🔢 Generate pitch values from user-defined range
def generate_pitch_list(start, end, step):
    pitches = []
    current = start
    while current <= end + 1e-9:
        pitches.append(round(current, 4))
        current += step
    return pitches

# 🧼 Format numbers for display (e.g., 5.0 → "5")
def format_number(val):
    return str(int(val)) if val == int(val) else str(val)

# 🧵 Thread object to store calculated dimensions
class Thread:
    def __init__(self):
        self.gender = None
        self.thread_class = None
        self.major_dia = 0.0
        self.pitch_dia = 0.0
        self.minor_dia = 0.0
        self.tap_drill = None

# 🧩 Abstract base class for thread profiles
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

# 🧵 Metric thread generator class
class MetricThreadGenerator(ThreadProfile):
    class Designation:
        def __init__(self, diameter, pitch):
            self.nominal_diameter = diameter
            self.pitch = pitch
            self.name = f"M{format_number(diameter)}x{format_number(pitch)}"

    def __init__(self, pitch_list):
        self.pitches = pitch_list

    def sizes(self):
        return thread_sizes

    def designations(self, size):
        return [self.Designation(size, pitch) for pitch in self.pitches]

    def threads(self, designation):
        threads = []
        P = designation.pitch
        D = designation.nominal_diameter
        H = (P / 2) / math.tan(math.radians(thread_angle / 2))
        pitch_dia = D - 2 * (3 * H / 8)
        minor_dia = D - 2 * (5 * H / 8)

        for offset in tolerance_offsets:
            class_label = f"O.{str(offset)[2:]}"  # e.g., 0.1 → "O.1"

            # External thread
            ext = Thread()
            ext.gender = "external"
            ext.thread_class = class_label
            ext.major_dia = D - offset
            ext.pitch_dia = pitch_dia - offset
            ext.minor_dia = minor_dia - offset
            threads.append(ext)

            # Internal thread
            int_thread = Thread()
            int_thread.gender = "internal"
            int_thread.thread_class = class_label
            int_thread.major_dia = D + offset
            int_thread.pitch_dia = pitch_dia + offset
            int_thread.minor_dia = minor_dia + offset
            int_thread.tap_drill = D - P
            threads.append(int_thread)

        return threads

# 🧾 XML generator function
def generate_xml():
    pitch_list = generate_pitch_list(pitch_start, pitch_end, pitch_step)
    profile = MetricThreadGenerator(pitch_list)

    root = ET.Element("ThreadType")
    tree = ET.ElementTree(root)

    # Add metadata
    ET.SubElement(root, "Name").text = thread_name
    ET.SubElement(root, "CustomName").text = thread_name
    ET.SubElement(root, "Unit").text = unit
    ET.SubElement(root, "Angle").text = str(thread_angle)
    ET.SubElement(root, "SortOrder").text = "3"

    # Add thread sizes and designations
    for size in profile.sizes():
        size_elem = ET.SubElement(root, "ThreadSize")
        ET.SubElement(size_elem, "Size").text = str(size)
        for designation in profile.designations(size):
            des_elem = ET.SubElement(size_elem, "Designation")
            ET.SubElement(des_elem, "ThreadDesignation").text = designation.name
            ET.SubElement(des_elem, "CTD").text = designation.name
            ET.SubElement(des_elem, "Pitch").text = str(designation.pitch)
            for thread in profile.threads(designation):
                thread_elem = ET.SubElement(des_elem, "Thread")
                ET.SubElement(thread_elem, "Gender").text = thread.gender
                ET.SubElement(thread_elem, "Class").text = thread.thread_class
                ET.SubElement(thread_elem, "MajorDia").text = f"{thread.major_dia:.4g}"
                ET.SubElement(thread_elem, "PitchDia").text = f"{thread.pitch_dia:.4g}"
                ET.SubElement(thread_elem, "MinorDia").text = f"{thread.minor_dia:.4g}"
                if thread.tap_drill is not None:
                    ET.SubElement(thread_elem, "TapDrill").text = f"{thread.tap_drill:.4g}"

    ET.indent(tree)
    tree.write(output_filename, encoding="UTF-8", xml_declaration=True)

# 🚀 Run the generator
if __name__ == "__main__":
    generate_xml()
    print(f"✅ XML file '{output_filename}' created for pitches from {pitch_start} mm to {pitch_end} mm in {pitch_step} mm steps.")

