import logging
import pytest
from pathlib import Path


# Hook to set up a log file specific to each test script
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    test_name = item.nodeid.split("::")[0].replace("/", "_").replace("\\", "_")
    log_dir = Path("Tests/Outputs/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{test_name}.log"

    # Configure a file handler for the test-specific log
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Add the handler to the root logger
    logger = logging.getLogger()
    logger.handlers = []  # Clear existing handlers to prevent duplicates
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


# Hook to set the report filename dynamically based on the test script
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    report_dir = Path("Tests/Outputs/report")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "Report.html"

    # Dynamically set the HTML report path
    session.config.option.htmlpath = str(report_file)