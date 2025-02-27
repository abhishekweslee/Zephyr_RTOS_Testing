# Zephyr RTOS Test Automation Project

## Introduction
Zephyr RTOS is a scalable and lightweight real-time operating system designed for embedded systems. This project aims to automate testing for various Zephyr RTOS features, including kernel functionality, inter-task communication, memory management, synchronization, timing, and performance. 

This repository provides a structured approach to:
- Setting up the Zephyr RTOS environment automatically using a Makefile.
- Running test cases to validate Zephyr functionalities.
- Logging test results and generating reports.

## Cloning the Repository
To get started, clone the project repository from GitHub and navigate to the project directory:

```sh
# Clone the repository
git clone https://github.com/abhishekweslee/Zephyr_RTOS_Test_Automation.git

# Change to the project directory
cd Zephyr_RTOS_Test_Automation
```

## Project Structure
```
Zephyr_RTOS_Test_Automation/
│-- Framework/
│   │-- Utils/
│   │   │-- zephyrproject/ (Zephyr RTOS setup directory)
│   │-- Libraries/
│   │   │-- requirements.txt (Python dependencies)
│   │-- Test_Scripts/ (Contains all test scripts)
│-- Inputs/
│   │-- Sample_Zephyr_Project/
│   │   │-- CMakeLists.txt
│   │   │-- prj.conf
│   │   │-- src/
│-- Makefile (Automates Zephyr RTOS environment setup)
│-- README.md (This file)
```

## Setting Up Zephyr RTOS Using Makefile
This project provides a `Makefile` to automate the installation of dependencies, setting up Zephyr RTOS, and configuring the required environment. 

### Step 1: Install System Dependencies
Run the following command to install all required system packages:

```sh
make setup_deps
```
This will:
- Update and upgrade the package lists.
- Install required dependencies, such as `git`, `cmake`, `ninja-build`, `python3`, `stlink-tools`, and more.
- Verify installed versions of `cmake`, `python`, and `dtc`.

### Step 2: Set Up Zephyr Project
Run the command:

```sh
make setup_zephyr
```
This will:
- Create a Python virtual environment (`.venv`) inside `zephyrproject/`.
- Install `west`, the Zephyr project manager.
- Initialize Zephyr in `zephyrproject/`.
- Update and export Zephyr dependencies.
- Install additional required Python packages.

### Step 3: Install Zephyr SDK
Run:

```sh
make install_sdk
```
This will:
- Install the Zephyr Software Development Kit (SDK).
- Grant necessary permissions to the Zephyr directory.

### Step 4: Verify Installation
Once the setup is complete, verify that `west` is working correctly by running:

```sh
./zephyrproject/.venv/bin/west --version
```
This should return the installed `west` version.

### Cleaning the Environment
To remove the Zephyr RTOS setup and start fresh, run:

```sh
make clean
```
This command deletes the `zephyrproject/` directory and removes all installed dependencies.

### Running the Entire Setup
To execute all setup steps in one command:

```sh
make all
```
This runs `setup_deps`, `setup_zephyr`, and `install_sdk` in sequence.

## Modifying Kconfig.zephyr
After running the `Makefile`, you need to modify the Zephyr configuration file to enable semaphore support.

Add the following lines to `Zephyr_RTOS_Test_Automation/Framework/Utils/zephyrproject/zephyr/Kconfig.zephyr`:

```plaintext
config SEMAPHORE
    bool "Enable Semaphore feature"
    default y
```

## Setting Up Python Virtual Environment
A Python virtual environment is used to manage dependencies.

### Step 1: Create a Virtual Environment
Run the following command in the project root directory:

```sh
python3 -m venv .venv
```

### Step 2: Activate the Virtual Environment
On Linux:
```sh
source .venv/bin/activate
```

### Step 3: Install Required Python Packages
Run:
```sh
pip install -r Framework/Libraries/requirements.txt
```
This installs all necessary Python dependencies for the testing framework.

### Deactivating the Virtual Environment
To exit the virtual environment, use:

```sh
deactivate
```

## Sample Zephyr Project Structure (Inputs Directory)
A sample Zephyr project is provided in the `Inputs` directory. The structure includes:

```
Sample_Zephyr_Project/
│-- CMakeLists.txt (Build configuration)
│-- prj.conf (Project-specific settings)
│-- src/
│   │-- main.c (Main application code)
```

- `CMakeLists.txt` specifies build settings and dependencies.
- `prj.conf` defines project-specific configurations.
- `src/main.c` contains the main Zephyr application logic.

## Running Tests
### Run All Tests
To execute all test cases:
```sh
pytest -s Tests/Test_Scripts/
```

### Run a Specific Test
To run an individual test script:
```sh
pytest -s Tests/Test_Scripts/<test_script>.py
```

## Test Logs, Reports, and Output Files
After running the tests, logs and reports are generated in the `Logs/` directory:
```
Logs/
│-- test_log_<timestamp>.log  (Detailed execution logs)
│-- reports/
│   │-- test_report_<timestamp>.html  (Formatted test report)
│-- output/
│   │-- test_output_<timestamp>.txt  (Raw test output)
```
- **Logs** contain execution details.
- **Reports** provide an overview of test results.
- **Output** stores the raw outputs of the test scripts.

## OS Compatibility
This project was designed and tested on Ubuntu 22.04.5 LTS. Its compatibility with other operating systems is not guaranteed.

## Conclusion
This repository provides a fully automated setup and testing framework for Zephyr RTOS. By following the steps outlined above, you can set up the environment, modify configurations, run tests, and analyze results efficiently.
