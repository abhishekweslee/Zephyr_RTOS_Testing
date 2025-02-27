import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR008")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR008", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_mutex_lock_unlock(setup_fixture):
    """Test mutex handling with priority inheritance."""
    output_file_path = "Tests/Outputs/Output_files/TZR008.txt"
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
    assert "Mutex Test: Started" in output_text, "Test did not start as expected."
    logger.info("Verified test start.")

    # Verify low-priority task acquires mutex first
    assert "[Low] Attempting to acquire mutex" in output_text, "Low-priority task did not attempt mutex acquisition."
    assert "[Low] Acquired mutex" in output_text, "Low-priority task did not acquire mutex."
    logger.info("Verified low-priority task mutex acquisition.")

    # Verify high-priority task attempts to acquire mutex while low-priority holds it
    assert "[High] Attempting to acquire mutex" in output_text, "High-priority task did not attempt mutex acquisition."
    low_acquire_index = output_text.find("[Low] Acquired mutex")
    high_attempt_index = output_text.find("[High] Attempting to acquire mutex")
    assert low_acquire_index < high_attempt_index, "High-priority task attempted mutex acquisition before low-priority acquired it."
    logger.info("Verified high-priority task attempts mutex acquisition after low-priority acquires it.")

    # Verify priority inheritance (high-priority task acquires mutex after low-priority releases it)
    assert "[Low] Releasing mutex" in output_text, "Low-priority task did not release mutex."
    low_release_index = output_text.find("[Low] Releasing mutex")
    high_acquire_index = output_text.find("[High] Acquired mutex")
    assert low_release_index < high_acquire_index, "High-priority task did not acquire mutex after low-priority released it."
    logger.info("Verified priority inheritance and mutex acquisition by high-priority task.")

    # Verify no deadlock (high-priority task releases mutex eventually)
    assert "[High] Releasing mutex" in output_text, "High-priority task did not release mutex, possible deadlock."
    logger.info("Verified no deadlock occurred.")

    # Verify medium-priority task runs in parallel
    medium_runs = len(re.findall(r"\[Medium\] Running", output_text))
    assert medium_runs >= 10, f"Expected medium-priority task to run multiple times, but found {medium_runs} occurrences."
    logger.info(f"Verified medium-priority task ran {medium_runs} times during the test.")

    logger.info("Test completed successfully. Mutex handling with priority inheritance validated.")
