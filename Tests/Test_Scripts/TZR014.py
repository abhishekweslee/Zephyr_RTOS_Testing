import pytest
import logging
from test_setup import TestSetup
import os
import sys
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TZR014")

@pytest.fixture(scope="function")
def setup_fixture(request):
    """Fixture to set up and clean up the test environment."""
    setup = TestSetup()
    setup.setup_method("TZR014", logger)

    yield setup  # Yield control to the test function

    setup.cleanup()  # Only deletes the folder

def isr_execution_time_test(setup_fixture):
    """Verify the execution time of the ISR (Interrupt Service Routine)."""
    output_file_path = "Tests/Outputs/Output_files/TZR014.txt"
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
    assert "Zephyr ISR Execution Time Test" in output_text, \
        "ISR execution time test did not start."
    logger.info("Verified ISR execution time test start.")

    # Verify CPU frequency extraction
    cpu_freq_match = re.search(r"CPU Frequency: (\d+) Hz", output_text)
    assert cpu_freq_match, "CPU frequency not found in the output."
    cpu_freq = int(cpu_freq_match.group(1))
    logger.info(f"Verified CPU frequency: {cpu_freq} Hz")

    # Verify ISR executed and end_time captured
    isr_executed_match = re.search(r"ISR Executed: end_time = (\d+)", output_text)
    assert isr_executed_match, "ISR execution not detected."
    end_time = int(isr_executed_match.group(1))
    logger.info(f"Verified ISR execution with end_time: {end_time}")

    # Verify ISR execution time is logged
    isr_time_match = re.search(r"ISR Execution Time: (\d+) ns", output_text)
    assert isr_time_match, "ISR execution time not logged."
    isr_execution_time_ns = int(isr_time_match.group(1))
    logger.info(f"Verified ISR execution time: {isr_execution_time_ns} ns")

    # Validate ISR execution time within acceptable limit (example: < 2000 ns)
    max_allowed_time_ns = 2000
    assert isr_execution_time_ns <= max_allowed_time_ns, \
        f"ISR execution time exceeded limit: {isr_execution_time_ns} ns > {max_allowed_time_ns} ns"
    logger.info(f"ISR execution time is within the acceptable limit ({max_allowed_time_ns} ns).")

    logger.info("Test completed successfully. ISR completed within expected time frame.")

