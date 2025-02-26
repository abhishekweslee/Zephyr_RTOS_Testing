import re


class ZephyrLogProcessor:
    """
    Processes Zephyr OS log files to extract data from the last occurrence of a boot pattern.
    """

    def __init__(self, pattern="*** Booting Zephyr OS"):
        """
        Initialize with a boot pattern.
        :param pattern: The pattern to search for in the log file.
        """
        self.pattern = pattern

    def extract_from_last_boot(self, file_path: str):
        """
        Extracts data starting from the last occurrence of the specified pattern to the end of the file.
        Handles partial matches and leaves the file unchanged if no match or partial match is found.

        :param file_path: Path to the log file to be processed.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Find all indices where the pattern fully matches at the start of a line
            full_match_indices = [i for i, line in enumerate(lines) if line.strip().startswith(self.pattern)]

            if full_match_indices:
                # Use the last full match index to extract from that line onwards
                start_index = full_match_indices[-1]
                new_data = lines[start_index:]
                print(f"Full pattern match found at line {start_index + 1}.")

            else:
                # Attempt partial match if no full match is found
                partial_match_indices = [i for i, line in enumerate(lines) if self.pattern in line]

                if partial_match_indices:
                    start_index = partial_match_indices[-1]

                    # Reconstruct the matched pattern line from the beginning
                    reconstructed_line = self.pattern + "\n"
                    new_data = [reconstructed_line] + lines[start_index + 1:]
                    print(f"Partial pattern match found at line {start_index + 1}. Pattern reconstructed.")
                else:
                    print(" No pattern or partial pattern found. File remains unchanged.")
                    return  # Exit without modifying the file

            # Overwrite the file with the new extracted data
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(new_data)

            print("File successfully updated.")

        except FileNotFoundError:
            print(f" File not found: {file_path}")
        except Exception as e:
            print(f" An error occurred: {e}")

    def _find_last_occurrence(self, content, pattern):
        """Finds the last occurrence of the exact pattern."""
        for i in range(len(content) - 1, -1, -1):
            if pattern in content[i]:
                return i
        return None

    def _find_partial_occurrence(self, content):
        """
        Finds the last occurrence of a partial pattern using regex for flexibility.
        Adjusts for potential glitches in serial data.
        """
        partial_regex = re.compile(re.escape(self.partial_pattern), re.IGNORECASE)
        for i in range(len(content) - 1, -1, -1):
            if partial_regex.search(content[i]):
                return i
        return None
