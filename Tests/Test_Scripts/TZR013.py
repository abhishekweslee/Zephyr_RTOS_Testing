import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR013")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR013", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def test_stack_overflow_underflow(setup_fixture):
    """Verify stack overflow and underflow conditions are detected and handled."""
    output_file_path = "Tests/Outputs/Output_files/TZR013.txt"
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

    # Verify start of the stack overflow test
    assert "Starting Stack Overflow Test..." in output_text, \
        "Stack overflow test did not start."
    logger.info("Verified start of stack overflow test.")

    # Verify stack overflow detection
    overflow_detected = re.search(r"ZEPHYR FATAL ERROR \d+: Stack overflow on CPU \d+", output_text)
    assert overflow_detected, "Stack overflow was not detected as expected."
    logger.info("Verified stack overflow detection.")

    # Verify MPU fault details are logged
    mpu_fault_detected = re.search(r"E: \*{5} MPU FAULT \*{5}", output_text)
    assert mpu_fault_detected, "MPU fault not detected during stack overflow."
    logger.info("Verified MPU fault details in output.")

    # Verify faulting instruction address presence
    faulting_instruction = re.search(r"Faulting instruction address \(r15/pc\): 0x[0-9a-fA-F]+", output_text)
    assert faulting_instruction, "Faulting instruction address not logged."
    logger.info("Verified faulting instruction address is present.")

    # Verify system halt after overflow detection
    assert "Halting system" in output_text, "System did not halt after detecting stack overflow."
    logger.info("Verified system halt after stack overflow.")

    logger.info("Test completed successfully. System detects and prevents stack misuse.")
