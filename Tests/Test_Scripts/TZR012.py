import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR012")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR012", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_case(setup_fixture):
    """Check out-of-memory (OOM) handling during continuous memory allocation."""
    output_file_path = "Tests/Outputs/Output_files/TZR012.txt"
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

    # Verify start of OOM test
    assert "Starting out-of-memory test..." in output_text, \
        "Out-of-memory test did not start."
    logger.info("Verified start of out-of-memory test.")

    # Verify continuous memory allocation until failure
    alloc_matches = re.findall(r"Allocated block (\d+) at address: (0x[0-9a-fA-F]+)", output_text)
    assert len(alloc_matches) > 0, "No memory blocks were allocated."
    logger.info(f"Allocated {len(alloc_matches)} memory blocks successfully.")

    # Verify out-of-memory condition handling
    oom_match = re.search(r"Out of memory! Allocation failed after (\d+) blocks\.", output_text)
    assert oom_match, "Out-of-memory condition not detected or message missing."
    allocated_blocks = int(oom_match.group(1))
    assert allocated_blocks == len(alloc_matches), \
        f"Mismatch in allocated block count. Reported: {allocated_blocks}, Detected: {len(alloc_matches)}"
    logger.info(f"Verified out-of-memory handling after {allocated_blocks} allocations.")

    # Verify completion message
    assert "Out-of-memory test completed." in output_text, \
        "Test did not complete as expected."
    logger.info("Verified completion of out-of-memory test without crash.")

    logger.info("Test completed successfully. System handles OOM conditions gracefully.")