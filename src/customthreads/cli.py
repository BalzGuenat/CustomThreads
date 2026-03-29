"""Command-line interface for thread generation."""

from .generator import generate_xml


def main():
    """Main entry point for CLI thread generation."""
    # ============================================================
    # 🚀 USER INPUT SECTION — START HERE
    # Change the values below to customize your thread generation
    # ============================================================

    # 🔧 Pitch range settings (in millimeters)
    pitch_start = 1.0  # Starting pitch value (e.g., 1.0 mm)
    pitch_end = 6.0  # Ending pitch value (e.g., 6.0 mm)
    pitch_step = 0.5  # Interval between pitches (e.g., 0.5 mm)

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

    # 🔧 Thread form code (for XML)
    thread_form = 8

    # ============================================================
    # 🚫 USER INPUT SECTION — END HERE
    # You don't need to change anything below this line
    # ============================================================

    generate_xml(
        output_filename=output_filename,
        thread_name=thread_name,
        unit=unit,
        thread_angle=thread_angle,
        thread_form=thread_form,
        pitch_start=pitch_start,
        pitch_end=pitch_end,
        pitch_step=pitch_step,
        thread_sizes=thread_sizes,
        tolerance_offsets=tolerance_offsets,
    )
    
    print(f"✅ XML file '{output_filename}' created for pitches from {pitch_start} mm to {pitch_end} mm in {pitch_step} mm steps.")


if __name__ == "__main__":
    main()
