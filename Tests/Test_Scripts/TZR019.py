import pytest
import logging
from test_setup import TestSetup
import os
import sys

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

def test_case_1(setup_fixture):
    """Example test case using the fixture."""
    # Your test logic here
    logger.info("Executing test_case_19")
    assert True  # Dummy assertion

