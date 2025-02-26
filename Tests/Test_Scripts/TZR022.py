import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR022")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR022", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_case(setup_fixture):
    """Test CPU usage measurement under varying task loads."""
    output_file_path = "Tests/Outputs/Output_files/TZR022.txt"
    logger.info(f"Reading output file: {output_file_path}")

    # Read the output file
    try:
        with open(output_file_path, "r") as file:
            output_text = file.read()
            logger.info("Output file read successfully.")
    except FileNotFoundError:
        logger.error(f"Output file not found at: {output_file_path}")
        pytest.fail(f"Output file not found at: {output_file_path}")

    # Verify Zephyr boot message
    assert "*** Booting Zephyr OS ***" in output_text, "Zephyr OS boot message not found."
    logger.info("Verified Zephyr OS boot message.")

    # Extract and verify CPU usage cycles
    cpu_usage_pattern = r"CPU Usage:\s*(\d+)\s*cycles"
    cpu_cycles = [int(match) for match in re.findall(cpu_usage_pattern, output_text)]
    assert cpu_cycles, "No CPU usage data found."
    logger.info(f"Extracted CPU usage cycles: {cpu_cycles}")

    # Verify increasing CPU usage over time
    assert all(earlier <= later for earlier, later in zip(cpu_cycles, cpu_cycles[1:])), \
        "CPU usage cycles did not consistently increase."
    logger.info("Verified CPU usage consistently increases over time.")

    # Verify CPU usage reaches saturation (≥ 1,000,000 cycles)
    assert any(cycle >= 1_000_000 for cycle in cpu_cycles), \
        "CPU usage did not reach expected saturation (≥ 1,000,000 cycles)."
    logger.info("Verified CPU usage reaches expected saturation.")