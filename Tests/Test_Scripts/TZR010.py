import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZ0010")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR010", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_dynamic_memory_allocation(setup_fixture):
    """Test dynamic memory allocation and deallocation without leaks."""
    output_file_path = "Tests/Outputs/Output_files/TZR010.txt"
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

    # Verify start of memory allocation test
    assert "Testing dynamic memory allocation..." in output_text, "Dynamic memory allocation test did not start."
    logger.info("Verified start of memory allocation test.")

    # Verify successful memory allocation
    match_alloc = re.search(r"Memory allocated at address: (0x[0-9a-fA-F]+)", output_text)
    assert match_alloc, "Memory allocation failed or was not reported."
    logger.info(f"Verified memory allocated at address: {match_alloc.group(1)}")

    # Verify memory allocation and data verification success
    assert "Memory allocation and verification successful!" in output_text, \
        "Memory data verification failed."
    logger.info("Verified memory allocation and data integrity.")

    # Verify memory was freed successfully
    assert "Memory freed successfully." in output_text, "Memory was not freed successfully."
    logger.info("Verified successful memory deallocation.")

    logger.info("Test completed successfully. Dynamic memory allocation and deallocation validated.")
