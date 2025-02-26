import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR011")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR011", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def memory_fragmentation_test(setup_fixture):
    """Validate memory fragmentation behavior during dynamic allocation."""
    output_file_path = "Tests/Outputs/Output_files/TZR011.txt"
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

    # Verify start of memory fragmentation test
    assert "Starting memory fragmentation test..." in output_text, \
        "Memory fragmentation test did not start."
    logger.info("Verified start of memory fragmentation test.")

    # Verify memory allocations
    alloc_matches = re.findall(r"Allocated block (\d+) at address: (0x[0-9a-fA-F]+)", output_text)
    assert len(alloc_matches) == 10, f"Expected 10 allocated blocks, found {len(alloc_matches)}."
    logger.info(f"Verified allocation of 10 memory blocks at addresses: {[addr for _, addr in alloc_matches]}")

    # Verify freeing of alternate blocks
    freed_blocks = re.findall(r"Freed block (\d+)", output_text)
    expected_freed = ['0', '2', '4', '6', '8']
    assert all(block in freed_blocks for block in expected_freed), \
        f"Expected freed blocks: {expected_freed}, but found: {freed_blocks}"
    logger.info(f"Verified freeing of alternate blocks: {expected_freed}")

    # Verify large block allocation after fragmentation
    large_block_match = re.search(r"Successfully allocated large block at: (0x[0-9a-fA-F]+)", output_text)
    assert large_block_match, "Large block allocation failed. Fragmentation may be too high."
    logger.info(f"Verified successful large block allocation at: {large_block_match.group(1)}")

    # Verify freeing of remaining blocks
    remaining_freed_blocks = ['1', '3', '5', '7', '9']
    assert all(block in freed_blocks for block in remaining_freed_blocks), \
        f"Expected remaining freed blocks: {remaining_freed_blocks}, but found: {freed_blocks}"
    logger.info(f"Verified freeing of remaining blocks: {remaining_freed_blocks}")

    # Verify completion message
    assert "Memory fragmentation test completed." in output_text, \
        "Memory fragmentation test did not complete as expected."
    logger.info("Verified completion of memory fragmentation test.")

    logger.info("Test completed successfully. Memory fragmentation behavior validated.")
