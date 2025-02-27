import pytest
import logging
from test_setup import TestSetup
import os
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TZR001")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    logger.info("Setting up the test environment.")
    setup = TestSetup()
    setup.setup_method("TZR001", logger)

    yield setup  # Yield control to the test function

    logger.info("Cleaning up the test environment.")
    setup.cleanup()


def test_task_management(setup_fixture):
    logger.info("Starting test_case_2.")

    output_file_path = "Tests/Outputs/Output_files/TZR001.txt"
    logger.info(f"Attempting to read the output file from: {output_file_path}")

    try:
        with open(output_file_path, "r") as file:
            output_text = file.read()
            logger.info("Output file read successfully.")
    except FileNotFoundError:
        logger.error(f"Output file not found at: {output_file_path}")
        assert False, f"Output file not found at: {output_file_path}"
    except Exception as e:
        logger.error(f"An error occurred while reading the output file: {e}")
        assert False, f"An error occurred while reading the output file: {e}"

    # Verify that the test has started
    logger.info("Verifying if the test has started.")
    assert "Task Management Test Started" in output_text, "Test did not start as expected."
    logger.info("Test start verified successfully.")

    # Pattern to capture thread start logs with priorities
    thread_start_pattern = re.compile(r"Thread (\d) started with (\w+) priority")
    thread_starts = thread_start_pattern.findall(output_text)
    logger.info(f"Captured thread start logs: {thread_starts}")

    expected_threads = [('1', 'HIGH'), ('2', 'MEDIUM'), ('3', 'LOW')]
    logger.info(f"Expected thread priorities: {expected_threads}")

    assert sorted(thread_starts) == sorted(expected_threads), (
        f"Thread start patterns do not match expected priorities. Found: {thread_starts}"
    )
    logger.info("Thread start patterns matched the expected priorities.")

    # Verify that each thread exits properly
    for thread_num in ['1', '2', '3']:
        logger.info(f"Verifying exit log for Thread {thread_num}.")
        assert f"Thread {thread_num} exiting..." in output_text, f"Thread {thread_num} did not exit as expected."
    logger.info("All threads exited as expected.")

    # Check the deletion sequence for all threads
    for thread_num in ['1', '2', '3']:
        logger.info(f"Verifying deletion log for Thread {thread_num}.")
        assert f"Deleting Thread {thread_num}..." in output_text, f"Thread {thread_num} was not deleted as expected."
    logger.info("All threads were deleted as expected.")

    # Verify test completion
    logger.info("Verifying test completion.")
    assert "Task Management Test Completed" in output_text, "Test did not complete successfully."
    logger.info("Test completed successfully.")
