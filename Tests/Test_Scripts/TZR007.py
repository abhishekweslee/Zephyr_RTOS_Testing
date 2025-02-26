import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR007")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR007", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_case(setup_fixture):
    logger.info("Starting semaphore test case.")

    output_file_path = "Tests/Outputs/Output_files/TZR007.txt"
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

    # Verify test start
    logger.info("Verifying test start.")
    assert "Semaphore Test: Started" in output_text, "Test did not start as expected."
    logger.info("Test start verified successfully.")

    # Extract semaphore events
    event_pattern = re.compile(
        r"<inf> semaphore_test: (?P<thread>Thread [A-C]): (?P<event>Attempting to acquire semaphore|Acquired semaphore|Released semaphore)"
    )
    events = event_pattern.findall(output_text)
    logger.info(f"Extracted events: {events}")
    assert events, "No semaphore events found in the output."

    semaphore_holder = None
    thread_states = {}

    for thread, event in events:
        logger.info(f"Processing event: {thread} - {event}")

        if event == "Attempting to acquire semaphore":
            thread_states[thread] = "attempting"

        elif event == "Acquired semaphore":
            # Exclusive access validation
            assert semaphore_holder is None, f"{thread} acquired semaphore while {semaphore_holder} was holding it."
            assert thread_states.get(thread) == "attempting", f"{thread} acquired semaphore without attempting first."
            semaphore_holder = thread
            thread_states[thread] = "acquired"
            logger.info(f"{thread} acquired semaphore successfully.")

        elif event == "Released semaphore":
            # Validate release after acquire
            assert semaphore_holder == thread, f"{thread} released semaphore without holding it."
            assert thread_states.get(thread) == "acquired", f"{thread} released semaphore without acquiring it."
            semaphore_holder = None
            thread_states[thread] = "released"
            logger.info(f"{thread} released semaphore successfully.")

    # Final validation to ensure semaphore is not held at the end
    assert semaphore_holder is None, "Semaphore was still held at the end of the test."
    logger.info("Semaphore was properly released at the end of the test.")

    logger.info("Test completed successfully.")