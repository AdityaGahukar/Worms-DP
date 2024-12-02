import os
import time
import random
import shutil
import sys
import subprocess
import psutil

# Safe mode for testing
TEST_MODE = True  # Ensure this is enabled to restrict worm behavior.
File_Execution = True  # Allow automatic execution of replicated files.
BASE_DIRS = 5  # Reduced number of base directories for testing.
SPREAD_POWER = 2  # Adjusted replication multiplier.
EXECUTE = True  # Enable code execution.
CODE = """print("Hello from the worm!")"""  # Simple payload for testing.
CODE_TYPE = "PYTHON"  # Type of payload.
SELF_PATH = sys.argv[0]  # Path of the current script
TARGET_PROCESS_NAME = os.path.basename(sys.argv[0])  # Process name to monitor and protect.

# Define controlled test path
TEST_PATH = "D:\\TestWormFolder"  # Change this to your desired test folder

# Stopping mechanism
STOP_TIME = 3  # Worm will stop after 5 seconds
START_TIME = time.time()  # Record the start time

def trigger_bsod():
    """Triggers a BSOD (disabled for testing)."""
    print("Simulating BSOD (disabled in test mode).")

def create_test_folder():
    """Creates the base test folder if it doesn't exist."""
    if not os.path.exists(TEST_PATH):
        os.makedirs(TEST_PATH)
        print(f"Test folder created at: {TEST_PATH}")

DIRS = []  # Track created directories
FILE_PATHS = []  # Track created file paths

def write_code_to_file(directory):
    """Writes the CODE content to a Python file in the given directory."""
    file_path = os.path.join(directory, "payload.py")
    try:
        with open(file_path, "w") as f:
            f.write(CODE)
        print(f"Python file created: {file_path}")
    except Exception as e:
        print(f"Error writing Python file: {e}")
    return file_path

def execute_code(file_path):
    """Executes the given Python file."""
    try:
        subprocess.run(["python", file_path], check=True)
        print(f"Executed: {file_path}")
    except Exception as e:
        print(f"Error executing file {file_path}: {e}")

def main():
    print("Worm Test Mode Activated")
    create_test_folder()
    print(f"Script Path: {SELF_PATH}")
    time.sleep(1)

    # Controlled spreading
    while time.time() - START_TIME < STOP_TIME:  # Stop after STOP_TIME seconds
        for i in range(BASE_DIRS * SPREAD_POWER):
            dir_name = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=10)) + "_WORM"
            dir_path = os.path.join(TEST_PATH, dir_name)
            DIRS.append(dir_path)

            try:
                os.makedirs(dir_path)  # Copy itself
                payload_path = write_code_to_file(dir_path)  # Write the CODE to a Python file
                if File_Execution and EXECUTE:
                    execute_code(payload_path)  # Execute the Python file
                print(f"Replicated in: {dir_path}")
            except Exception as e:
                print(f"Error creating directory: {e}")

        time.sleep(2)  # Pause between replication cycles

    print("Stopping worm replication after timeout.")

    # Notify user that the script is waiting for input
    print("Waiting for user to press Enter to begin cleanup...")

    # Wait for user input to proceed with cleanup
    input("Press Enter to begin cleanup...")

    cleanup()


def cleanup():
    """Clean up all created directories."""
    for directory in DIRS:
        try:
            shutil.rmtree(directory)
            print(f"Removed: {directory}")
        except Exception as e:
            print(f"Error removing directory: {e}")
    print("Cleanup complete.")

def monitor_task():
    """Monitor for process and trigger BSOD if the script is killed (disabled in test mode)."""
    process_exists = True
    while process_exists:
        process_exists = any(proc.name() == TARGET_PROCESS_NAME for proc in psutil.process_iter())
        if not process_exists:
            print(f"Process '{TARGET_PROCESS_NAME}' was killed. Simulated BSOD.")
            trigger_bsod()
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "EXECUTE":
        pass
    else:
        main()
