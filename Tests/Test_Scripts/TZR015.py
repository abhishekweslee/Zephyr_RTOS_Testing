import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR015")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR015", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def nested_interrupts_handling(setup_fixture):
    """Test nested interrupts and priority-based handling."""
    output_file_path = "Tests/Outputs/Output_files/TZR015.txt"
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
    assert "Zephyr Nested IRQ Test with 5 Levels" in output_text, \
        "Nested IRQ test did not start."
    logger.info("Verified nested IRQ test start.")

    # Verify IRQ trigger sequence
    irq_sequence = [
        "Triggering IRQ1...",
        "IRQ1 Executed, triggering IRQ2...",
        "IRQ2 Executed, triggering IRQ3...",
        "IRQ3 Executed, triggering IRQ4...",
        "IRQ4 Executed, triggering IRQ5...",
        "IRQ5 (Highest Priority) Executed"
    ]

    for irq_msg in irq_sequence:
        assert irq_msg in output_text, f"Missing expected IRQ message: '{irq_msg}'"
        logger.info(f"Verified IRQ message: '{irq_msg}'")

    # Verify final test result
    assert "Nested Interrupt Test Passed: Execution order verified." in output_text, \
        "Nested interrupt test did not pass as expected."
    logger.info("Verified successful nested interrupt test completion.")

    logger.info("Test completed successfully. Higher-priority interrupts preempted lower ones as expected.")






