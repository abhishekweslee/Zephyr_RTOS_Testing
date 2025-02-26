import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR017")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR017", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_case(setup_fixture):
    """Test to validate timer creation, deletion, and expiry handling."""
    output_file_path = "Tests/Outputs/Output_files/TZR017.txt"
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

    # Verify Zephyr OS boot
    assert "*** Booting Zephyr OS" in output_text, "Zephyr OS did not boot as expected."
    logger.info("Verified Zephyr OS boot.")

    # Verify test start message
    assert "Starting Timer Creation, Deletion & Expiry Test..." in output_text, \
        "Timer test did not start as expected."
    logger.info("Verified test start message.")

    # Verify timer initialization
    assert "Timer initialized successfully." in output_text, \
        "Timer was not initialized successfully."
    logger.info("Verified timer initialization.")

    # Verify timer start
    assert "Timer started: 1000 ms timeout, 500 ms period." in output_text, \
        "Timer did not start with the expected timeout and period."
    logger.info("Verified timer start with correct parameters.")

    # Verify timer expiry callback
    assert "Timer expired! Callback executed." in output_text, \
        "Timer expiry callback was not executed."
    logger.info("Verified timer expiry callback execution.")

    # Verify test pass message
    assert "Test Passed: Timer expired as expected." in output_text, \
        "Test did not pass or timer did not expire as expected."
    logger.info("Verified successful timer expiry.")

    # Verify timer stop and deletion
    assert "Timer stopped." in output_text, "Timer was not stopped."
    assert "Timer stopped and deleted." in output_text, "Timer was not deleted."
    logger.info("Verified timer stop and deletion.")

    logger.info("Test completed successfully. Timer handled creation, expiry, and deletion as expected.")