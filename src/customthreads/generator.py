"""XML generation and utility functions for thread generators."""

import xml.etree.ElementTree as ET
from .models import MetricThreadGenerator
from .utils import format_number


def generate_pitch_list(start, end, step):
    """Generate pitch values from user-defined range.
    
    Args:
        start: Starting pitch value in mm
        end: Ending pitch value in mm
        step: Interval between pitches in mm
        
    Returns:
        List of pitch values (rounded to 4 decimals)
    """
    pitches = []
    current = start
    while current <= end + 1e-9:
        pitches.append(round(current, 4))
        current += step
    return pitches


def generate_xml(
    output_filename,
    thread_name,
    unit,
    thread_angle,
    thread_form,
    pitch_start,
    pitch_end,
    pitch_step,
    thread_sizes,
    tolerance_offsets,
):
    """Generate XML file with thread specifications.
    
    Args:
        output_filename: Name of output XML file
        thread_name: Display name of thread type
        unit: Unit of measurement (usually "mm")
        thread_angle: Thread angle in degrees (usually 60.0)
        thread_form: Thread form code (usually 8)
        pitch_start: Starting pitch value
        pitch_end: Ending pitch value
        pitch_step: Pitch step interval
        thread_sizes: List of thread diameters to generate
        tolerance_offsets: List of tolerance offsets
    """
    pitch_list = generate_pitch_list(pitch_start, pitch_end, pitch_step)
    profile = MetricThreadGenerator(
        pitch_list, thread_sizes, tolerance_offsets, thread_angle
    )

    root = ET.Element("ThreadType")
    tree = ET.ElementTree(root)

    ET.SubElement(root, "Name").text = thread_name
    ET.SubElement(root, "CustomName").text = thread_name
    ET.SubElement(root, "Unit").text = unit
    ET.SubElement(root, "Angle").text = str(thread_angle)
    ET.SubElement(root, "ThreadForm").text = str(thread_form)
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
                ET.SubElement(thread_element, "MajorDia").text = f"{thread.majorDia:.4g}"
                ET.SubElement(thread_element, "PitchDia").text = f"{thread.pitchDia:.4g}"
                ET.SubElement(thread_element, "MinorDia").text = f"{thread.minorDia:.4g}"
                if thread.tapDrill is not None:
                    ET.SubElement(thread_element, "TapDrill").text = f"{thread.tapDrill:.4g}"

    ET.indent(tree)
    tree.write(output_filename, encoding="UTF-8", xml_declaration=True)
