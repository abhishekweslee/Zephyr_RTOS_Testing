import os
import sys
import logging
import time

# Adding the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.Serial_connect import SerialReader
from Framework.Core.folder_manager import FolderManager
from Framework.Core.Builder import Builder

logger = logging.getLogger(__name__)
FM = FolderManager(
    source_folder="Tests/Inputs/TZR001/",
    destination_folder="Framework/Utils/zephyrproject/zephyr/TZR001/"
)
FM.copy_folder()
FM.grant_permissions()
time.sleep(10)
builder = Builder(
    toolchain_location=".venv/bin/west",
    board_name="nucleo_f401re",
    project_location="zephyr/TZR001",
    bin_file_location="build/zephyr/zephyr.bin",
    logger=logger
)
builder.build_project()
time.sleep(5)
builder.flash_firmware()
time.sleep(5)

SC = SerialReader(serial_port="/dev/ttyACM4", output_file="Tests/Outputs/TZR001/Output_files/output.txt", baud_rate= 15200, logger=logger)
SC.start_reading()

status = builder.reset_board()  # Ensure `builder` is properly defined before calling this
print("+++++++++++++++",status,"+++++++++++++++++")
time.sleep(10)

SC.stop_reading()
