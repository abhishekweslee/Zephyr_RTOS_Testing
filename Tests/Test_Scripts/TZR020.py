import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR020")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR020", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def resource_contention_simulation(setup_fixture):
    """Test to validate resource contention handling between tasks."""
    output_file_path = "Tests/Outputs/Output_files/TZR020.txt"
    logger.info(f"Reading output file: {output_file_path}")

    # Read the output file
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

    # Verify simulation start message
    assert "Starting Resource Contention Simulation..." in output_text, "Test did not start as expected."
    logger.info("Verified test start message.")

    # Regex patterns for resource access
    waiting_pattern = r"Thread ([AB]): Waiting to acquire resource\.\.\."
    acquired_pattern = r"Thread ([AB]): Acquired resource, working\.\.\."
    released_pattern = r"Thread ([AB]): Releasing resource\."

    # Compile regex pattern
    pattern = re.compile(
        rf"({waiting_pattern})|({acquired_pattern})|({released_pattern})"
    )

    events = []
    for match in pattern.finditer(output_text):
        if match.group(2):  # Waiting pattern matched
            events.append(("waiting", match.group(2)))
        elif match.group(4):  # Acquired pattern matched
            events.append(("acquired", match.group(4)))
        elif match.group(6):  # Released pattern matched
            events.append(("released", match.group(6)))

    # Ensure both threads attempted to acquire the resource
    waiting_threads = [thread for event, thread in events if event == "waiting"]
    assert "A" in waiting_threads, "Thread A did not attempt to acquire the resource."
    assert "B" in waiting_threads, "Thread B did not attempt to acquire the resource."
    logger.info("Both threads attempted to acquire the resource.")

    # ✅ Check the number of acquire and release events match
    acquired_count = sum(1 for event, _ in events if event == "acquired")
    released_count = sum(1 for event, _ in events if event == "released")
    assert acquired_count == released_count, (
        f"Mismatched acquire ({acquired_count}) and release ({released_count}) events."
    )
    logger.info(f"Verified acquire and release events are balanced: {acquired_count} occurrences each.")
