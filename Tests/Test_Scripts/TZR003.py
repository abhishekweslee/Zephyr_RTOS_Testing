import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR003")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR003", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_context_switching(setup_fixture):
    """Test to validate context switching time from Zephyr RTOS output."""
    output_file_path = "Tests/Outputs/Output_files/TZR003.txt"
    logger.info(f"Reading output file: {output_file_path}")

    try:
        with open(output_file_path, "r") as file:
            output_text = file.read()
            logger.info("Output file read successfully.")
    except FileNotFoundError:
        logger.error(f"Output file not found at: {output_file_path}")
        pytest.fail(f"Output file not found at: {output_file_path}")
    except Exception as e:
        logger.error(f"Error reading output file: {e}")
        pytest.fail(f"Error reading output file: {e}")

    # Verify test start
    assert "Starting Context Switching Test..." in output_text, "Test did not start as expected."
    logger.info("Verified test start.")

    # Extract context switch times using regex
    pattern = r"context_switch: Context switch time: (\d+) cycles"
    matches = re.findall(pattern, output_text)
    logger.info(f"Captured context switch times: {matches}")

    # Ensure context switch times are found
    assert matches, "No context switch times found in the output."

    switch_times = [int(time) for time in matches]
    min_cycles, max_cycles = 42000000, 42008000

    # Validate each context switch time
    for index, time in enumerate(switch_times, start=1):
        assert min_cycles <= time <= max_cycles, (
            f"Test {index}: FAIL - Context switch time {time} cycles out of range [{min_cycles}, {max_cycles}]."
        )
        logger.info(f"Test {index}: PASS - Context switch time {time} cycles within expected range.")

    logger.info("Test completed successfully. Context switching times validated.")

