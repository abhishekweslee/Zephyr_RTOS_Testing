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
    setup.setup_method("TZR004", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_task_state_transition(setup_fixture):
    """Test correct task state transitions (Ready, Running, Blocked, Suspended)."""
    output_file_path = "Tests/Outputs/Output_files/TZR004.txt"
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

    # Verify test start and thread creation
    assert "Starting Task State Transition Test..." in output_text, "Test did not start as expected."
    logger.info("Verified test start.")
    assert "Threads created, scheduling will now begin..." in output_text, "Thread creation message missing."
    logger.info("Verified thread creation.")

    # Expected states for each task
    task_states = {
        "High Priority Task": ["READY state", "RUNNING state"],
        "Medium Priority Task": ["READY state", "BLOCKED state", "RUNNING state after unblocking"],
        "Low Priority Task": ["READY state", "SUSPENDING Medium Priority Task", "RESUMING Medium Priority Task", "RUNNING state"]
    }

    # Verify all expected states appear in the output
    for task, states in task_states.items():
        for state in states:
            pattern = re.escape(f"{task}: {state}")
            assert re.search(pattern, output_text), f"Missing state '{state}' for {task}."
            logger.info(f"Verified state '{state}' for {task}.")

    # Verify semaphore release and Medium Priority Task wake-up
    assert "Releasing Semaphore - Medium Priority Task will wake up" in output_text, "Semaphore release message missing."
    logger.info("Verified semaphore release.")
    assert "Medium Priority Task: RUNNING state after unblocking" in output_text, "Medium Priority Task did not resume after semaphore release."
    logger.info("Verified Medium Priority Task resumed after unblocking.")

    # Verify suspension and resumption of Medium Priority Task
    assert "Low Priority Task: SUSPENDING Medium Priority Task" in output_text, "Medium Priority Task was not suspended."
    logger.info("Verified Medium Priority Task suspension.")
    assert "Low Priority Task: RESUMING Medium Priority Task" in output_text, "Medium Priority Task was not resumed."
    logger.info("Verified Medium Priority Task resumption.")

    logger.info("Test completed successfully. Task state transitions validated.")
