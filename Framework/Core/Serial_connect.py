import serial
import threading
import time
import logging


class Serial_connect:
    def __init__(self, port, baud_rate, output_file, logger):
        self.port = port
        self.baud_rate = baud_rate
        self.output_file = output_file
        self.logger = logger
        self.running = False
        self.thread = None
        self.serial_conn = self._init_serial()

    def _init_serial(self):
        attempts = 0
        while attempts < 3:
            try:
                self.logger.info(f"Attempting to open serial port {self.port}, attempt {attempts + 1}")
                return serial.Serial(self.port, self.baud_rate, timeout=1)
            except serial.SerialException as e:
                self.logger.error(f"Attempt {attempts + 1}: Failed to open serial port {self.port}. Error: {e}")
                attempts += 1
                time.sleep(2)
        self.logger.critical(f"Failed to open serial port {self.port} after 3 attempts.")
        raise Exception(f"Failed to open serial port {self.port} after 3 attempts.")

    def _write_to_file(self, line):
        try:
            with open(self.output_file, 'a') as file:
                file.write(line + '\n')
            self.logger.debug(f"Written to file: {line}")
        except IOError as e:
            self.logger.error(f"Error writing to file {self.output_file}: {e}")

    def read_by_time(self, delay):
        self.logger.info(f"Reading serial data for {delay} seconds")
        end_time = time.time() + delay
        while time.time() < end_time:
            if self.serial_conn and self.serial_conn.in_waiting:
                line = self.serial_conn.readline().decode(errors='ignore').strip()
                self._write_to_file(line)

    def read_by_lines(self, num_lines):
        self.logger.info(f"Reading {num_lines} lines from serial port")
        count = 0
        while count < num_lines:
            if self.serial_conn and self.serial_conn.in_waiting:
                line = self.serial_conn.readline().decode(errors='ignore').strip()
                self._write_to_file(line)
                count += 1

    def _continuous_read(self):
        self.logger.info("Starting continuous serial read")
        while self.running:
            if self.serial_conn and self.serial_conn.in_waiting:
                line = self.serial_conn.readline().decode(errors='ignore').strip()
                self._write_to_file(line)
        self.logger.info("Stopping continuous serial read")

    def serial_start(self):
        if not self.running:
            self.logger.info("Starting serial read thread")
            self.running = True
            self.thread = threading.Thread(target=self._continuous_read)
            self.thread.start()

    def serial_stop(self):
        if self.running:
            self.logger.info("Stopping serial read thread")
            self.running = False
            if self.thread:
                self.thread.join()

    def close(self):
        if self.serial_conn:
            self.logger.info("Closing serial connection")
            self.serial_conn.close()

# Example Usage
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
# serial_conn = Serial_connect('/dev/ttyUSB0', 115200, 'output.txt', logger)
# serial_conn.serial_start()
# time.sleep(10)  # Read continuously for 10 seconds
# serial_conn.serial_stop()
# serial_conn.close()
