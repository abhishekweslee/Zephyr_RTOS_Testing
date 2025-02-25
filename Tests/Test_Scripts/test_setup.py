import os
import sys
import logging
import time

# Ensure the Framework directory is in the Python path before importing its modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.Serial_connect import SerialReader
from Framework.Core.folder_manager import FolderManager
from Framework.Core.Builder import Builder


class TestSetup:
    def setup_method(self, file_name, logger=None):
        self.file_name = file_name
        self.logger = logger or logging.getLogger(file_name)  # Use provided logger or create one

        self.FM = FolderManager(
            source_folder=f"Tests/Inputs/{file_name}/",
            destination_folder=f"Framework/Utils/zephyrproject/zephyr/{file_name}/"
        )
        self.FM.copy_folder()
        self.FM.grant_permissions()
        time.sleep(10)
        builder = Builder(
            toolchain_location=".venv/bin/west",
            board_name="nucleo_f401re",
            project_location=f"zephyr/{file_name}",
            bin_file_location="build/zephyr/zephyr.bin",
            logger=self.logger
        )
        builder.build_project()
        time.sleep(5)
        builder.flash_firmware()
        time.sleep(5)

        self.SC = SerialReader(
            serial_port="/dev/ttyACM4",
            output_file=f"Tests/Outputs/Output_files/{file_name}.txt",
            baud_rate=115200,
            logger=self.logger
        )
        self.SC.start_reading()

        status = builder.reset_board()
        print(status)
        self.logger.info(f"Board reset status {status}")
        time.sleep(10)

        self.SC.stop_reading()

    def cleanup(self):
        """Cleanup after the test execution."""
        self.logger.info("Cleaning up for %s", self.file_name)
        self.FM.delete_folder()  # Only delete the folder in cleanup
