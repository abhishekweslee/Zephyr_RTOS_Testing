import subprocess
import re

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

# Example usage
if __name__ == "__main__":
    status = run_st_flash()
    print("Final Result:", status)
