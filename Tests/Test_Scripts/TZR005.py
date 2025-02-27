import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR005")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR005", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_task_starvation_priority_inversion(setup_fixture):
    """Test to validate task starvation prevention and priority inversion handling."""
    output_file = "Tests/Outputs/Output_files/TZR005.txt"
    try:
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.fail(f"Output file {output_file} does not exist.")

        with open(output_file, 'r') as file:
            content = file.read()

        # Validate essential messages for task starvation and priority inversion
        required_messages = [
            "Starting Task Starvation & Priority Inversion Test",
            "Low-Priority Task: Trying to acquire Mutex",
            "Low-Priority Task: Holding Mutex",
            "High-Priority Task Running",
            "Low-Priority Task: Releasing Mutex"
        ]

        for message in required_messages:
            assert message in content, f"Required message not found: '{message}'"

        logger.info("All required messages for task starvation and priority inversion are present.")

    finally:
        # Cleanup
        logger.info("Test TZR004 completed successfully.")

