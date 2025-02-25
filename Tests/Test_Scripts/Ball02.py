import serial
import threading
import subprocess
import re
import time

# Serial port configuration (Update according to your STM32 board)
SERIAL_PORT = "/dev/ttyACM0"  # Change as per your device
BAUD_RATE = 115200  # Default baud rate of STM32F401RE
OUTPUT_FILE = "serial_dance.txt"

# Global variables
ser = None
reading_thread = None
stop_thread = False

# ANSI Escape Code Removal Regex
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def strip_ansi_codes(text):
    """Removes ANSI escape codes from the given text."""
    return ANSI_ESCAPE_PATTERN.sub('', text)


def run_st_flash():
    try:
        # Run the command and capture output
        result = subprocess.run(
            ["st-flash", "--connect-under-reset", "reset"],
            text=True,
            capture_output=True,
            check=True
        )

        # Merge stdout and stderr (in case output is split)
        actual_output = (result.stdout + result.stderr).strip()
        print("Actual Output:\n", actual_output)  # Debugging

        # Expected pattern
        pattern = r"st-flash 1\.7\.0(\n.*)?"

        if re.fullmatch(pattern, actual_output, re.DOTALL):
            return "OK"
        else:
            return "FAIL"

    except subprocess.CalledProcessError as e:
        print("Command failed with error:", e.stderr)
        return "FAIL"


def read_serial():
    """Function to read data from serial and write to console and file."""
    global stop_thread, ser

    try:
        with open(OUTPUT_FILE, "w") as file:
            while not stop_thread:
                try:
                    if ser.in_waiting > 0:
                        data = ser.readline().decode("utf-8", errors="ignore").strip()
                        clean_data = strip_ansi_codes(data)  # Remove ANSI codes
                        print(clean_data)  # Print to console
                        file.write(clean_data + "\n")  # Write to file
                        file.flush()
                except serial.SerialException:
                    print("Serial device disconnected!")
                    break
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break
    except IOError as e:
        print(f"File error: {e}")


def start_reading():
    """Starts the serial reading process in a separate thread."""
    global ser, reading_thread, stop_thread

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        stop_thread = False
        reading_thread = threading.Thread(target=read_serial, daemon=True)
        reading_thread.start()
        print(f"Started reading from {SERIAL_PORT}...")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")


def stop_reading():
    """Stops the serial reading process."""
    global ser, stop_thread
    stop_thread = True
    if ser:
        ser.close()
        ser = None
    print("Stopped reading serial data.")


# Example usage:
if __name__ == "__main__":
    start_reading()
    time.sleep(2)  # Give time for serial to initialize

    status = run_st_flash()
    print("Final Result:", status)

    time.sleep(10)  # Delay before stopping
    stop_reading()  # Stop reading automatically after the delay
