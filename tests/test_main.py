import pytest
import xml.etree.ElementTree as ET
from customthreads import (
    MetricThreadGenerator,
    generate_pitch_list,
    format_number,
)
from customthreads.generator import generate_xml


class TestThreadGeneration:
    """Integration tests for thread XML generation."""

    def test_pitch_list_generation(self):
        """Test that pitch_list is generated correctly."""
        pitches = generate_pitch_list(1.0, 2.0, 0.5)
        assert pitches == [1.0, 1.5, 2.0]

    def test_pitch_list_edge_case(self):
        """Test pitch list generation with floating point edge cases."""
        pitches = generate_pitch_list(1.0, 3.5, 0.5)
        assert len(pitches) == 6
        assert pitches[0] == 1.0
        assert pitches[-1] == 3.5

    def test_format_number_integer(self):
        """Test format_number removes .0 from integers."""
        assert format_number(5.0) == "5"
        assert format_number(10.0) == "10"

    def test_format_number_decimal(self):
        """Test format_number preserves decimals."""
        assert format_number(5.5) == "5.5"
        assert format_number(2.75) == "2.75"

    def test_xml_generation_default_config(self, tmp_path):
        """Test XML generation with default configuration."""
        output = tmp_path / "test_output_1.xml"
        # Generate XML with test config
        generate_xml(
            output_filename=str(output),
            thread_name="Test Threads",
            unit="mm",
            thread_angle=60.0,
            thread_form=8,
            pitch_start=1.0,
            pitch_end=1.5,
            pitch_step=0.5,
            thread_sizes=list(range(8, 11)),
            tolerance_offsets=[0.0, 0.1],
        )

        # Verify file exists
        assert output.exists()

        # Parse and verify structure
        tree = ET.parse(output)
        root = tree.getroot()

        assert root.tag == "ThreadType"
        assert root.find("Name").text == "Test Threads"
        assert root.find("Unit").text == "mm"
        assert root.find("Angle").text == "60.0"
        assert root.find("ThreadForm").text == "8"

    def test_xml_thread_sizes(self, tmp_path):
        """Test that XML contains expected thread sizes."""
        output = tmp_path / "test_output_2.xml"
        generate_xml(
            output_filename=str(output),
            thread_name="Test Threads",
            unit="mm",
            thread_angle=60.0,
            thread_form=8,
            pitch_start=1.0,
            pitch_end=1.0,
            pitch_step=1.0,
            thread_sizes=list(range(8, 12)),
            tolerance_offsets=[0.0],
        )

        tree = ET.parse(output)
        root = tree.getroot()

        thread_sizes = root.findall("ThreadSize")
        assert len(thread_sizes) == 4

        # Verify size elements exist
        for size_elem in thread_sizes:
            size = size_elem.find("Size").text
            assert size is not None
            assert int(size) >= 8

    def test_xml_thread_designations(self, tmp_path):
        """Test that thread designations are correctly named."""
        output = tmp_path / "test_output_3.xml"
        generate_xml(
            output_filename=str(output),
            thread_name="Test Threads",
            unit="mm",
            thread_angle=60.0,
            thread_form=8,
            pitch_start=1.0,
            pitch_end=1.0,
            pitch_step=1.0,
            thread_sizes=list(range(8, 11)),
            tolerance_offsets=[0.0],
        )

        tree = ET.parse(output)
        root = tree.getroot()

        # Find designations
        designations = root.findall(".//Designation")
        assert len(designations) > 0

        # Check format of thread designation (should be like M8x1)
        for des in designations[:3]:
            des_text = des.find("ThreadDesignation").text
            assert "M" in des_text
            assert "x" in des_text

    def test_xml_contains_threads(self, tmp_path):
        """Test that XML contains external and internal threads."""
        output = tmp_path / "test_output_4.xml"
        generate_xml(
            output_filename=str(output),
            thread_name="Test Threads",
            unit="mm",
            thread_angle=60.0,
            thread_form=8,
            pitch_start=1.0,
            pitch_end=1.0,
            pitch_step=1.0,
            thread_sizes=list(range(8, 11)),
            tolerance_offsets=[0.0, 0.1],
        )

        tree = ET.parse(output)
        root = tree.getroot()

        threads = root.findall(".//Thread")
        assert len(threads) > 0

        # Check for both genders
        genders = {thread.find("Gender").text for thread in threads}
        assert {"external", "internal"}.issubset(genders)


class TestThreadProfile:
    """Tests for MetricThreadGenerator class."""

    def test_generator_initialization(self):
        """Test MetricThreadGenerator accepts configuration."""
        pitches = [1.0, 1.5, 2.0]
        sizes = list(range(8, 51))
        offsets = [0.0, 0.1]
        generator = MetricThreadGenerator(pitches, sizes, offsets, 60.0)
        assert generator.pitches == pitches

    def test_generator_sizes(self):
        """Test generator returns correct sizes."""
        sizes = list(range(8, 51))
        offsets = [0.0, 0.1]
        generator = MetricThreadGenerator([1.0], sizes, offsets, 60.0)
        gen_sizes = generator.sizes()
        assert len(gen_sizes) == len(sizes)
        assert gen_sizes[0] == 8

    def test_generator_designations(self):
        """Test generator creates designations for each size and pitch."""
        pitches = [1.0, 1.5]
        sizes = list(range(8, 51))
        offsets = [0.0, 0.1]
        generator = MetricThreadGenerator(pitches, sizes, offsets, 60.0)

        designations = generator.designations(10)
        assert len(designations) == 2
        assert designations[0].name == "M10x1"
        assert designations[1].name == "M10x1.5"

    def test_generator_threads(self):
        """Test generator creates threads for each tolerance offset."""
        pitches = [1.0]
        sizes = list(range(8, 51))
        offsets = [0.0, 0.1, 0.2, 0.4, 0.8]
        generator = MetricThreadGenerator(pitches, sizes, offsets, 60.0)

        des = MetricThreadGenerator.Designation(10, 1.0)
        threads = generator.threads(des)

        # Should have 2 threads per offset (external + internal) = 10 threads
        assert len(threads) == len(offsets) * 2
