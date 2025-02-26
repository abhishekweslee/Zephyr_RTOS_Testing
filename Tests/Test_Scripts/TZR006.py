import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR006")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR006", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_case(setup_fixture):
    """Test to validate message queue handling with different priorities."""

    output_file = "Tests/Outputs/Output_files/TZR006.txt"

    try:
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.fail(f"Output file {output_file} does not exist.")

        with open(output_file, 'r') as file:
            lines = file.readlines()

        # Verify initial message
        assert any("Starting Message Queue Priority Test" in line for line in lines), \
            "Start message not found in output."

        # Extract sent and received messages
        sent_pattern = re.compile(r"Sender Task \(Priority (-?\d+)\): Sent Message ID (\d+)")
        recv_pattern = re.compile(r"Receiver: Received Message ID (\d+) from Priority (-?\d+)")

        sent_messages = [(int(priority), int(msg_id)) for line in lines if (match := sent_pattern.search(line))
                         for priority, msg_id in [match.groups()]]
        received_messages = [(int(msg_id), int(priority)) for line in lines if (match := recv_pattern.search(line))
                              for msg_id, priority in [match.groups()]]

        assert sent_messages, "No sent messages found."
        assert received_messages, "No received messages found."

        # Group received messages by message ID
        received_by_id = {}
        for msg_id, priority in received_messages:
            received_by_id.setdefault(msg_id, []).append(priority)

        # Validate that messages are received in priority order: HIGH (-1) -> MEDIUM (0) -> LOW (1)
        expected_priority_order = [-1, 0, 1]
        for msg_id, priorities in received_by_id.items():
            assert priorities == expected_priority_order, (
                f"Incorrect priority order for Message ID {msg_id}. "
                f"Expected {expected_priority_order}, got {priorities}."
            )

        logger.info("Message queue handling validated successfully.")

    finally:
        # Cleanup
        logger.info("Test TZR006 completed successfully.")

