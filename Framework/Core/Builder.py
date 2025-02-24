import subprocess
import re
import os
import sys


class Builder:
    def __init__(self, toolchain_location, project_location, bin_file_location, board_name, logger):
        self.toolchain_location = toolchain_location
        self.project_location = project_location
        self.bin_file_location = bin_file_location
        self.board_name = board_name
        self.logger = logger

    def run_command(self, command):
        # Store the current working directory
        original_dir = os.getcwd()

        # Define the target directory (absolute or relative)
        target_dir = os.path.join(original_dir, "Framework", "Utils", "zephyrproject")

        try:
            # Change to the target directory
            os.chdir(target_dir)
            print(command)
            """Runs a command and returns the output"""
            self.logger.info(f"Executing command: {command}")
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Ensures output is treated as text
            )
            stdout, stderr = process.communicate()  # Wait for process completion

            # Log full command output
            self.logger.debug(f"Command output:\n{stdout}")
            self.logger.debug(f"Command errors:\n{stderr}")

            return stdout, stderr, process.returncode

        finally:
            # Restore the original working directory
            os.chdir(original_dir)

    def build_project(self):
        """Runs the build command and checks if it succeeded"""
        command = f"{self.toolchain_location} build -p always -b {self.board_name} {self.project_location}"
        output, _, returncode = self.run_command(command)

        # Check for the expected pattern in the full output
        pattern = r"Generating files from .+?zephyr\.elf for board: nucleo_f401re"
        if re.search(pattern, output):
            self.logger.info("Build process completed successfully!")
            return True
        else:
            self.logger.warning("Pattern not found. Retrying build once...")

            # Run the command again for retry
            output, _, returncode = self.run_command(command)

            # Print retry output for debugging
            print(f"Retry build attempt output:\n{output}")

            if re.search(pattern, output):
                self.logger.info("Build process succeeded on retry!")
                return True
            else:
                self.logger.error("Build process failed after retry.")
                return False

    def flash_firmware(self):
        """Flashes the firmware and ensures it's verified"""
        command = f"st-flash --connect-under-reset write {self.bin_file_location} 0x08000000"
        output, _, returncode = self.run_command(command)

        # Print full command output for debugging
        print(f"First flash attempt output:\n{output}")

        # Check for success pattern
        if "Flash written and verified! jolly good!" in output:
            self.logger.info("Firmware flashed successfully!")
            return True
        else:
            self.logger.warning("Firmware flash verification failed. Retrying once...")

            # Retry flashing
            output, _, returncode = self.run_command(command)

            # Print retry output for debugging
            print(f"Retry flash attempt output:\n{output}")

            if "Flash written and verified! jolly good!" in output:
                self.logger.info("Firmware flashed successfully on retry!")
                return True
            else:
                self.logger.error("Firmware flash failed after retry.")
                return False

    def reset_board(self):
        """Resets the board using st-flash"""
        command = "st-flash --connect-under-reset reset"
        output, _, returncode = self.run_command(command)

        # Print reset output for debugging
        print(f"Board reset output:\n{output}")

        if returncode == 0:
            self.logger.info("Board reset successfully!")
        else:
            self.logger.error("Board reset failed!")

