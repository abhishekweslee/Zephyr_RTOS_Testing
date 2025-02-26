import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR023")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR023", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def task_execution_time_profiling(setup_fixture):
    """Test task execution time profiling under varying system conditions."""
    output_file_path = "Tests/Outputs/Output_files/TZR023.txt"
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
    assert "*** Booting Zephyr OS: Task Execution Profiling ***" in output_text, \
        "Zephyr OS boot message not found."
    logger.info("Verified Zephyr OS boot message.")

    # Verify monitor task status messages
    monitor_pattern = r"\[Monitor\] System running\.\.\."
    monitor_messages = re.findall(monitor_pattern, output_text)
    assert len(monitor_messages) >= 1, "Monitor task messages not found."
    logger.info(f"Found {len(monitor_messages)} monitor task status messages.")

    # Extract execution times for each task
    task_patterns = {
        "High Load Task": r"High Load Task executed in (\d+) cycles",
        "Medium Load Task": r"Medium Load Task executed in (\d+) cycles",
        "Low Load Task": r"Low Load Task executed in (\d+) cycles",
    }

    task_execution_times = {}
    for task_name, pattern in task_patterns.items():
        cycles = [int(match) for match in re.findall(pattern, output_text)]
        assert cycles, f"{task_name} execution times not found."
        task_execution_times[task_name] = cycles
        logger.info(f"{task_name} execution times: {cycles}")

    # Verify execution times are consistent (small variance)
    for task_name, cycles in task_execution_times.items():
        mean = sum(cycles) / len(cycles)
        max_deviation = max(abs(cycle - mean) for cycle in cycles)
        allowed_deviation = mean * 0.05  # Allow 5% variance
        assert max_deviation <= allowed_deviation, \
            f"{task_name} execution times vary beyond acceptable range."
        logger.info(f"{task_name} execution times within acceptable variance.")

    # Verify execution order (High Load > Medium Load > Low Load)
    for high, medium, low in zip(
        task_execution_times["High Load Task"],
        task_execution_times["Medium Load Task"],
        task_execution_times["Low Load Task"]
    ):
        assert high > medium > low, \
            f"Execution time order incorrect: High({high}) ≤ Medium({medium}) ≤ Low({low})"
    logger.info("Verified correct execution time ordering: High > Medium > Low.")
