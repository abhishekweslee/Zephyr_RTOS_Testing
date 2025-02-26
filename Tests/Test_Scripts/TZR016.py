import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR016")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR016", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_case(setup_fixture):
    """Test to ensure ISR does not block indefinitely or cause a deadlock."""
    output_file_path = "Tests/Outputs/Output_files/TZR016.txt"
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

    # Verify test start message
    assert "Starting ISR deadlock test..." in output_text, \
        "ISR deadlock test did not start."
    logger.info("Verified ISR deadlock test start.")

    # Verify software interrupt trigger
    assert "Triggering software interrupt..." in output_text, \
        "Software interrupt was not triggered."
    logger.info("Verified software interrupt trigger.")

    # Verify ISR execution
    assert "ISR executed!" in output_text, \
        "ISR did not execute, potential deadlock detected."
    logger.info("Verified ISR execution without deadlock.")

    logger.info("Test completed successfully. ISRs executed without deadlock as expected.")