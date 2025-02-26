import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR024")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR024", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def periodic_task_deadline_adherence(setup_fixture):
    """Test to validate real-time deadline adherence for periodic tasks."""
    output_file_path = "Tests/Outputs/Output_files/TZR024.txt"
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

    # Patterns to extract task start times, jitters, and missed deadlines
    task_start_pattern = re.compile(r"Task started at (\d+) ms \(Jitter: (-?\d+) ms\)")
    task_complete_pattern = re.compile(r"Task completed at (\d+) ms, execution time: (\d+) ms")
    missed_deadline_pattern = re.compile(r"Missed deadline by (\d+) ms")

    task_starts = task_start_pattern.findall(output_text)
    task_completions = task_complete_pattern.findall(output_text)
    missed_deadlines = missed_deadline_pattern.findall(output_text)

    logger.info(f"Total task starts: {len(task_starts)}")
    logger.info(f"Total task completions: {len(task_completions)}")
    logger.info(f"Missed deadlines: {len(missed_deadlines)}")

    # Validation parameters
    acceptable_jitter_ms = 5
    expected_execution_time = 200
    execution_tolerance = 10
    max_allowed_missed_deadlines = 0

    # Validate jitter for task starts
    for idx, (start_time, jitter) in enumerate(task_starts, start=1):
        jitter = int(jitter)
        logger.info(f"Task {idx}: Start jitter = {jitter} ms")
        assert abs(jitter) <= acceptable_jitter_ms, f"Task {idx} jitter {jitter} ms exceeds acceptable limit."

    # Validate execution times
    for idx, (_, exec_time) in enumerate(task_completions, start=1):
        exec_time = int(exec_time)
        logger.info(f"Task {idx}: Execution time = {exec_time} ms")
        assert abs(exec_time - expected_execution_time) <= execution_tolerance, \
            f"Task {idx} execution time {exec_time} ms out of acceptable range."

    # Validate missed deadlines
    assert len(missed_deadlines) <= max_allowed_missed_deadlines, \
        f"Missed deadlines: {len(missed_deadlines)} exceed allowed limit of {max_allowed_missed_deadlines}."

    logger.info("Test completed successfully. Real-time deadlines validated.")
