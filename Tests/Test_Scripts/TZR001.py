import pytest
import os
import sys
import logging
import time

# Adding the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.Serial_connect import Serial_connect
from Framework.Core.folder_manager import FolderManager
from Framework.Core.Builder import Builder

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def built():
    FM = FolderManager(source_folder="Tests/Inputs/TZR001/",
                       destination_folder="Framework/Utils/zephyrproject/zephyr/TZR001/")
    FM.copy_folder()
    FM.grant_permissions()
    time.sleep(10)
    builder = Builder(toolchain_location=".venv/bin/west",
                      board_name="nucleo_f401re",
                      project_location="zephyr/TZR001",
                      bin_file_location="zephyr/build/zephyr/zephyr.bin",
                      logger=logger)
    builder.build_project()
    time.sleep(5)
    builder.flash_firmware()
    time.sleep(5)
    yield builder

def test_sample(built):

    SC = Serial_connect(port="/dev/ttyACM0",
                        baud_rate="15200",
                        output_file="Tests/Outputs/Output_file/TZR001_output.txt",
                        logger=logger)

    SC.serial_start()
    built.reset_board()
    time.sleep(10)
    SC.serial_stop()