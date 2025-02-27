import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR002")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR002", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_task_scheduling(setup_fixture):
    """Test task switching and scheduling policies."""
    output_file_path = "Tests/Outputs/Output_files/TZR002.txt"
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

    # Verify that the test has started and threads were created
    assert "Starting Task Scheduling Test..." in output_text, "Test did not start as expected."
    logger.info("Verified test start.")
    assert "Threads created, scheduling will now begin..." in output_text, "Threads creation message missing."
    logger.info("Verified thread creation and scheduling start.")

    # Expected task run messages
    task_patterns = [
        "High Priority Task Running",
        "Medium Priority Task Running",
        "Low Priority Task Running"
    ]

    # Extract all task run logs in order
    task_run_pattern = re.compile(r"(High|Medium|Low) Priority Task Running")
    task_run_logs = task_run_pattern.findall(output_text)
    logger.info(f"Captured task run logs: {task_run_logs}")

    # Check that tasks have run multiple times
    for task in ["High", "Medium", "Low"]:
        occurrences = task_run_logs.count(task)
        assert occurrences > 1, f"{task} Priority Task did not run multiple times."
        logger.info(f"{task} Priority Task ran {occurrences} times.")

    # Verify task switching pattern
    logger.info("Verifying task switching sequence.")
    expected_cycle = ["High", "Medium", "Low"]
    cycles_detected = 0

    # Check if task_run_logs contains at least two complete cycles
    for i in range(len(task_run_logs) - 2):
        if task_run_logs[i:i+3] == expected_cycle:
            cycles_detected += 1

    assert cycles_detected >= 2, f"Task switching did not follow the expected cycle at least twice. Detected cycles: {cycles_detected}"
    logger.info(f"Detected {cycles_detected} complete task switching cycles.")

    logger.info("Test completed successfully. Task switching and scheduling policies validated.")
