import pytest
import logging
from test_setup import TestSetup
import os
import sys
import shutil
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR021")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR021", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_case(setup_fixture):
    """Test concurrent access to shared resources with and without mutex."""
    output_file_path = "Tests/Outputs/Output_files/TZR021.txt"
    logger.info(f"Reading output file: {output_file_path}")

    # Read output file
    try:
        with open(output_file_path, "r") as file:
            output_text = file.read()
            logger.info("Output file read successfully.")
    except FileNotFoundError:
        logger.error(f"Output file not found at: {output_file_path}")
        pytest.fail(f"Output file not found at: {output_file_path}")

    # Verify test start message
    assert "Starting Concurrent Access Test..." in output_text, "Test did not start as expected."
    logger.info("Verified test start message.")

    # Verify final resource value
    final_value_match = re.search(r"Final shared_resource value:\s*(\d+)", output_text)
    assert final_value_match, "Final shared_resource value not found."
    final_value = int(final_value_match.group(1))
    assert final_value == 15, f"Unexpected final shared_resource value: {final_value}"
    logger.info(f"Verified final shared_resource value: {final_value}")

    # Regex patterns
    unsafe_pattern = r"Unsafe: Thread ([AB]) updated shared_resource to (\d+)"
    safe_pattern = r"Safe: Thread ([CD]) updated shared_resource to (\d+)"

    unsafe_events = re.findall(unsafe_pattern, output_text)
    safe_events = re.findall(safe_pattern, output_text)

    # Verify unsafe access increments (allowing race conditions)
    assert unsafe_events, "No unsafe access events found."
    unsafe_values = [int(value) for _, value in unsafe_events]
    expected_unsafe_values = set(range(1, 6))

    # Check that all expected values appear at least once
    assert expected_unsafe_values.issubset(set(unsafe_values)), \
        f"Missing unsafe increments: {expected_unsafe_values - set(unsafe_values)}"
    logger.info(f"Verified unsafe increments: {sorted(set(unsafe_values))}")

    # Verify safe access increments (no race conditions expected)
    assert safe_events, "No safe access events found."
    safe_values = [int(value) for _, value in safe_events]
    expected_safe_values = list(range(6, 16))
    assert safe_values == expected_safe_values, f"Safe access sequence error: {safe_values}"
    logger.info(f"Verified safe increments: {safe_values}")