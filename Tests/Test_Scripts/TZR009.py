import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR009")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR009", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def event_flags_synchronization_test(setup_fixture):
    """Test event flags signalling and task synchronization."""
    output_file_path = "Tests/Outputs/Output_files/TZR009.txt"
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

    # Verify test boot and start
    assert "*** Booting Zephyr OS" in output_text, "Zephyr OS did not boot as expected."
    logger.info("Verified Zephyr OS boot.")

    # Verify the consumer waits for EVENT_FLAG_1
    assert "Waiting for EVENT_FLAG_1..." in output_text, "Consumer did not wait for EVENT_FLAG_1."
    logger.info("Verified consumer waiting for EVENT_FLAG_1.")

    # Verify the producer sets EVENT_FLAG_1
    assert "Setting EVENT_FLAG_1" in output_text, "Producer did not set EVENT_FLAG_1."
    logger.info("Verified producer sets EVENT_FLAG_1.")

    # Verify consumer receives EVENT_FLAG_1
    match_event_1 = re.search(r"Received EVENT_FLAG_1: 0x([0-9A-Fa-f]+)", output_text)
    assert match_event_1, "Consumer did not receive EVENT_FLAG_1."
    assert match_event_1.group(1) == "1", f"Expected EVENT_FLAG_1 value: 0x1, got: 0x{match_event_1.group(1)}"
    logger.info("Verified consumer received correct EVENT_FLAG_1 value.")

    # Verify the consumer waits for EVENT_FLAG_2
    assert "Waiting for EVENT_FLAG_2..." in output_text, "Consumer did not wait for EVENT_FLAG_2."
    logger.info("Verified consumer waiting for EVENT_FLAG_2.")

    # Verify the producer sets EVENT_FLAG_2
    assert "Setting EVENT_FLAG_2" in output_text, "Producer did not set EVENT_FLAG_2."
    logger.info("Verified producer sets EVENT_FLAG_2.")

    # Verify consumer receives EVENT_FLAG_2
    match_event_2 = re.search(r"Received EVENT_FLAG_2: 0x([0-9A-Fa-f]+)", output_text)
    assert match_event_2, "Consumer did not receive EVENT_FLAG_2."
    assert match_event_2.group(1) == "2", f"Expected EVENT_FLAG_2 value: 0x2, got: 0x{match_event_2.group(1)}"
    logger.info("Verified consumer received correct EVENT_FLAG_2 value.")

    # Verify synchronization sequence
    event_1_set_index = output_text.find("Setting EVENT_FLAG_1")
    event_1_received_index = output_text.find("Received EVENT_FLAG_1")
    event_2_set_index = output_text.find("Setting EVENT_FLAG_2")
    event_2_received_index = output_text.find("Received EVENT_FLAG_2")

    assert event_1_set_index < event_1_received_index, "EVENT_FLAG_1 was received before it was set."
    assert event_2_set_index < event_2_received_index, "EVENT_FLAG_2 was received before it was set."
    logger.info("Verified correct synchronization sequence between producer and consumer tasks.")

    logger.info("Test completed successfully. Event flags signalling and synchronization validated.")

