import os
import threading
import re
import logging
import time
import subprocess
import select


class SerialReader:
    def __init__(self, serial_port="/dev/ttyACM4", baud_rate=115200, output_file="Master_output.txt", logger=None,
                 timeout=5):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.output_file = output_file
        self.running = False
        self.thread = None
        self.timeout = timeout
        self.logger = logger if logger else logging.getLogger(__name__)

        # Configure serial port
        self._configure_serial_port()

    def _configure_serial_port(self):
        """Configures the serial port settings using `stty`."""
        try:
            if not os.path.exists(self.serial_port):
                raise FileNotFoundError(f"Serial port {self.serial_port} not found.")

            subprocess.run(["stty", "-F", self.serial_port, str(self.baud_rate)], check=True)
            self.logger.info(f"[INFO] Serial port {self.serial_port} configured with baud rate {self.baud_rate}.")
        except FileNotFoundError as e:
            self.logger.error(f"[ERROR] {e}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"[ERROR] Failed to configure serial port: {e}")
        except Exception as e:
            self.logger.error(f"[ERROR] Unexpected error in configuring serial port: {e}")

    def _remove_ansi_escape(self, text):
        """Removes ANSI escape codes from the input text."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def _read_serial(self):
        """Reads serial data continuously and writes to the file."""
        try:
            with open(self.serial_port, "rb") as f, open(self.output_file, "w", encoding="utf-8") as out_f:
                self.logger.info("[INFO] Serial reading started...")

                last_read_time = time.time()
                while self.running:
                    try:
                        fds, _, _ = select.select([f], [], [], self.timeout)  # Non-blocking check
                        if fds:
                            data = f.readline().decode(errors="ignore").strip()
                            if data:
                                clean_data = self._remove_ansi_escape(data)
                                print(clean_data)
                                out_f.write(clean_data + "\n")
                                out_f.flush()
                                last_read_time = time.time()
                    except Exception as e:
                        self.logger.error(f"[ERROR] Serial read error: {e}")
                        break

                    # Stop if no data received for `timeout` seconds
                    if time.time() - last_read_time > self.timeout:
                        self.logger.warning("[WARNING] No new data received. Stopping serial reader.")
                        self.running = False
                        break
        except FileNotFoundError:
            self.logger.error(f"[ERROR] Serial port {self.serial_port} not found.")
        except PermissionError:
            self.logger.error(f"[ERROR] Permission denied for {self.serial_port}. Try running as root.")
        except Exception as e:
            self.logger.error(f"[ERROR] {e}")
        finally:
            self.logger.info("[INFO] Closing serial reader.")

    def start_reading(self):
        """Starts the serial data reading process."""
        if not self.running:
            try:
                self.logger.info("[INFO] Starting serial data collection...")
                self.running = True
                self.thread = threading.Thread(target=self._read_serial, daemon=True)
                self.thread.start()
            except Exception as e:
                self.logger.error(f"[ERROR] Failed to start thread: {e}")
        else:
            self.logger.warning("[WARNING] Already running!")

    def stop_reading(self):
        """Stops the serial data reading process."""
        if self.running:
            try:
                self.logger.info("[INFO] Stopping serial data collection...")
                self.running = False
                if self.thread:
                    self.thread.join()
                self.logger.info(f"[INFO] Data saved to: {self.output_file}")
            except Exception as e:
                self.logger.error(f"[ERROR] Failed to stop thread: {e}")
        else:
            self.logger.warning("[WARNING] Not currently running!")


# Usage example:
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#     logger = logging.getLogger("SerialReader")
#
#     reader = SerialReader(serial_port="/dev/ttyACM0", baud_rate=115200, output_file="Master_output.txt", logger=logger,
#                           timeout=3)
#
#     reader.start_reading()
#
#     time.sleep(10)  # Read for 10 seconds (replace with your logic)
#
#     reader.stop_reading()
