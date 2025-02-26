import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR026")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR026", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_high_task_count_performance(setup_fixture):
    """Test to validate system performance under a high number of tasks without degradation."""
    output_file_path = "Tests/Outputs/Output_files/TZR026.txt"
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

    # Regular expression to capture task type and execution cycles
    pattern = re.compile(r"(High|Medium|Low) Load Task executed in (\d+) cycles")
    matches = pattern.findall(output_text)

    if not matches:
        logger.error("No task execution data found in the output.")
        pytest.fail("No task execution measurements were found in the output file.")

    # Expected cycle ranges for performance under high task count
    expected_ranges = {
        "High": (500000, 501000),
        "Medium": (100000, 101000),
        "Low": (50000, 51000),
    }

    # Validate each task execution time
    for task_type, cycles_str in matches:
        cycles = int(cycles_str)
        min_cycles, max_cycles = expected_ranges[task_type]
        logger.info(f"{task_type} Load Task executed in {cycles} cycles (Expected: {min_cycles}-{max_cycles} cycles)")
        assert min_cycles <= cycles <= max_cycles, (
            f"{task_type} Load Task cycles {cycles} out of expected range ({min_cycles}-{max_cycles})"
        )

    # Check for "[Monitor] System running..." messages to ensure system stability
    monitor_count = output_text.count("[Monitor] System running...")
    expected_monitor_count = 6  # Based on provided output
    logger.info(f"System monitor messages found: {monitor_count} (Expected: {expected_monitor_count})")
    assert monitor_count == expected_monitor_count, (
        f"Expected {expected_monitor_count} monitor messages, but found {monitor_count}."
    )

    logger.info("System handled high task count without degradation.")