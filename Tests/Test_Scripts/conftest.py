import os
import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Ensure test items are sorted to avoid random selection issues."""
    items.sort(key=lambda item: item.location[0])  # Sort test scripts alphabetically


@pytest.fixture(scope="function")
def output_dir(request):
    """Automatically determine output directory for each test script."""
    test_file = request.node.location[0]  # Get the current test file name
    script_name = os.path.splitext(os.path.basename(test_file))[0]  # Remove .py

    base_path = os.path.join("Tests", "Outputs", script_name)
    return base_path


def pytest_configure(config):
    """Create individual report and log directories for each test script."""
    test_files = set()

    # Check if running all tests or a specific test file
    if config.args:
        for test_file in config.args:
            if test_file.endswith(".py"):
                script_name = os.path.splitext(os.path.basename(test_file))[0]
                test_files.add(script_name)
    else:
        for item in config.pluginmanager.get_plugin("session").items:
            test_file = item.location[0]  # Get test file name
            script_name = os.path.splitext(os.path.basename(test_file))[0]  # Remove .py
            test_files.add(script_name)

    for script_name in test_files:
        base_path = os.path.join("Tests", "Outputs", script_name)
        report_dir = os.path.join(base_path, "report")
        log_dir = os.path.join(base_path, "logs")

        os.makedirs(report_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)

    print(f"\nCreated directories for test scripts: {sorted(test_files)}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Configure report and log paths dynamically for each test."""
    test_file = item.location[0]  # Get test script name
    script_name = os.path.splitext(os.path.basename(test_file))[0]  # Remove .py

    base_path = os.path.join("Tests", "Outputs", script_name)
    report_dir = os.path.join(base_path, "report")
    log_dir = os.path.join(base_path, "logs")

    item.config.option.htmlpath = os.path.join(report_dir, "test_report.html")
    item.config.option.log_file = os.path.join(log_dir, "test_log.log")
