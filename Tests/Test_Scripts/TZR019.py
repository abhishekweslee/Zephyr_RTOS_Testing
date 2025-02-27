import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR019")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR019", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_sleep_delay_accuracy_test(setup_fixture):
    """Test to measure the accuracy of sleep and delay functions."""
    output_file_path = "Tests/Outputs/Output_files/TZR019.txt"
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
    assert "Starting Sleep & Delay Accuracy Test..." in output_text, "Test did not start as expected."
    logger.info("Verified test start message.")

    # Validate k_sleep() accuracy
    sleep_match = re.search(r"k_sleep\(\) expected: (\d+) ms, actual: (\d+) ms", output_text)
    assert sleep_match, "k_sleep() timing log not found."

    expected_sleep = int(sleep_match.group(1))
    actual_sleep = int(sleep_match.group(2))
    sleep_drift = abs(actual_sleep - expected_sleep)
    logger.info(f"k_sleep(): Expected={expected_sleep} ms, Actual={actual_sleep} ms, Drift={sleep_drift} ms")
    assert sleep_drift <= 10, f"k_sleep() drift exceeded 10 ms: {sleep_drift} ms"

    # Validate k_busy_wait() accuracy
    busy_wait_match = re.search(r"k_busy_wait\(\) expected: (\d+) us, actual: (\d+) us", output_text)
    assert busy_wait_match, "k_busy_wait() timing log not found."

    expected_busy_wait = int(busy_wait_match.group(1))
    actual_busy_wait = int(busy_wait_match.group(2))
    busy_wait_drift = abs(actual_busy_wait - expected_busy_wait)
    logger.info(f"k_busy_wait(): Expected={expected_busy_wait} us, Actual={actual_busy_wait} us, Drift={busy_wait_drift} us")
    assert busy_wait_drift <= 1000, f"k_busy_wait() drift exceeded 1000 us: {busy_wait_drift} us"

    # Verify test completion
    assert "Test Completed." in output_text, "Test did not complete successfully."
    logger.info("Test completed successfully with acceptable sleep and delay accuracy.")
