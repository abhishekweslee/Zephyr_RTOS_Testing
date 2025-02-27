import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR018")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR018", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_timer_precision_validation(setup_fixture):
    """Test to validate the precision of periodic and one-shot timers."""
    output_file_path = "Tests/Outputs/Output_files/TZR018.txt"
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
    assert "Starting Timer Precision Test..." in output_text, "Timer precision test did not start as expected."
    logger.info("Verified test start message.")

    # Verify one-shot timer start
    assert "One-shot timer started: 1000 ms timeout" in output_text, "One-shot timer did not start with the expected timeout."
    logger.info("Verified one-shot timer start.")

    # Verify periodic timer start
    assert "Periodic timer started: 500 ms period" in output_text, "Periodic timer did not start with the expected period."
    logger.info("Verified periodic timer start.")

    # Check periodic timer expiry and precision
    periodic_expiry_matches = re.findall(r"Periodic timer expired! Expected: 500 ms, Actual: (\d+) ms", output_text)
    assert periodic_expiry_matches, "No periodic timer expiry logs found."
    logger.info(f"Found {len(periodic_expiry_matches)} periodic timer expiry logs.")

    for idx, actual_time_str in enumerate(periodic_expiry_matches, 1):
        actual_time = int(actual_time_str)
        drift = abs(actual_time - 500)
        logger.info(f"Periodic expiry #{idx}: Expected=500 ms, Actual={actual_time} ms, Drift={drift} ms")
        assert drift <= 10, f"Periodic timer drift exceeded 10 ms: {drift} ms"

    # Check one-shot timer expiry and precision
    oneshot_match = re.search(r"One-shot timer expired! Expected: 1000 ms, Actual: (\d+) ms", output_text)
    assert oneshot_match, "One-shot timer expiry log not found."

    oneshot_actual = int(oneshot_match.group(1))
    oneshot_drift = abs(oneshot_actual - 1000)
    logger.info(f"One-shot expiry: Expected=1000 ms, Actual={oneshot_actual} ms, Drift={oneshot_drift} ms")
    assert oneshot_drift <= 10, f"One-shot timer drift exceeded 10 ms: {oneshot_drift} ms"

    # Verify the final periodic timer trigger count
    periodic_count_match = re.search(r"Test completed\. Periodic timer triggered (\d+) times\.", output_text)
    assert periodic_count_match, "Final periodic timer trigger count log not found."

    periodic_trigger_count = int(periodic_count_match.group(1))
    logger.info(f"Periodic timer triggered {periodic_trigger_count} times.")
    assert periodic_trigger_count >= 5, f"Expected at least 5 periodic triggers, found {periodic_trigger_count}"

    logger.info("Test completed successfully. Timer precision within acceptable drift limits.")
