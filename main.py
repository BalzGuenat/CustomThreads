import math
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import json
import logging
import sys
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate XML files for custom threads.')
parser.add_argument('config_file', nargs='?', default='./config.json', help='Path to the configuration JSON file, default value is ./config.json')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
args = parser.parse_args()

# Set logging level based on verbose flag
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

# Load configurations from JSON file
with open(args.config_file, 'r') as file:
    profiles = json.load(file)['profiles']


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

    def __init__(self, sizes, pitches, offsets, angle):
        self._sizes = sizes
        self.pitches = pitches
        self.offsets = offsets
        self.angle = angle

    def sizes(self):
        return self._sizes

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def designations(self, size):
        return [self.Designation(size, pitch) for pitch in self.pitches]


    def threads(self, designation):
        threads = []
        for offset in self.offsets:
            offset_decimals = str(offset)[2:]  # skips the '0.' at the start
            # see https://en.wikipedia.org/wiki/ISO_metric_screw_thread
            P = designation.pitch
            H = 1/math.tan(math.radians(self.angle/2)) * (P/2)
            D = designation.nominalDiameter
            Dp = D - 2 * 3*H/8
            Dmin = D - 2 * 5*H/8

            t = Thread()
            t.gender = "external"
            t.clazz = "O.{}".format(offset_decimals)
            t.majorDia = D - offset
            t.pitchDia = Dp - offset
            t.minorDia = Dmin - offset
            threads.append(t)

            t = Thread()
            t.gender = "internal"
            t.clazz = "O.{}".format(offset_decimals)
            t.majorDia = D + offset
            t.pitchDia = Dp + offset
            t.minorDia = Dmin + offset
            t.tapDrill = D - P
            threads.append(t)
        return threads

def parse_sizes(sizes):
    if isinstance(sizes, str):
        if ':' in sizes:
            parts = sizes.split(',')
            start, end = map(int, parts[0].split(':'))
            step = int(parts[1]) if len(parts) > 1 else 1
            return list(range(start, end + 1, step))
    elif isinstance(sizes, list):
        return sizes
    else:
        raise ValueError("Invalid sizes format, should be a list or a range separated by ':'")

def generate_xml_files(profiles):
    for profile in profiles:
        name = profile['name']
        custom_name = profile.get('customName', name)
        unit = profile['unit']
        sizes = parse_sizes(profile['sizes'])
        angle = profile['angle']
        pitches = profile['pitches']
        offsets = profile['offsets']
        logging.info(f"Generating XML for {custom_name}")
        profile = Metric3Dprinted(sizes, pitches, offsets, angle)

        root = ET.Element('ThreadType')

        tree = ET.ElementTree(root)
        ET.SubElement(root, "Name").text = custom_name
        ET.SubElement(root, "CustomName").text = custom_name
        ET.SubElement(root, "Unit").text = unit

        ET.SubElement(root, "Angle").text = str(angle)
        ET.SubElement(root, "SortOrder").text = "3"
        for size in profile.sizes():
            logging.info(f"Processing size: {size}")
            thread_size_element = ET.SubElement(root, "ThreadSize")
            ET.SubElement(thread_size_element, "Size").text = str(size)
            for designation in profile.designations(size):
                designation_element = ET.SubElement(thread_size_element, "Designation")
                ET.SubElement(designation_element, "ThreadDesignation").text = designation.name
                ET.SubElement(designation_element, "CTD").text = designation.name
                ET.SubElement(designation_element, "Pitch").text = str(designation.pitch)
                for thread in profile.threads(designation):
                    logging.debug(f"Processing thread: Gender={thread.gender}, Class={thread.clazz}, MajorDia={thread.majorDia}, PitchDia={thread.pitchDia}, MinorDia={thread.minorDia}, TapDrill={thread.tapDrill}")
                    thread_element = ET.SubElement(designation_element, "Thread")
                    ET.SubElement(thread_element, "Gender").text = thread.gender
                    ET.SubElement(thread_element, "Class").text = thread.clazz
                    ET.SubElement(thread_element, "MajorDia").text = "{:.4g}".format(thread.majorDia)
                    ET.SubElement(thread_element, "PitchDia").text = "{:.4g}".format(thread.pitchDia)
                    ET.SubElement(thread_element, "MinorDia").text = "{:.4g}".format(thread.minorDia)
                    if thread.tapDrill:
                        ET.SubElement(thread_element, "TapDrill").text = "{:.4g}".format(thread.tapDrill)

        ET.indent(tree)
        tree.write(f"{name}.xml", encoding='UTF-8', xml_declaration=True)
        logging.info(f"XML file {name}.xml generated successfully")

# Example usage
generate_xml_files(profiles)
