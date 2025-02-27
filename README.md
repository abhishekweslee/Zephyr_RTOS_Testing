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
Zephyr_RTOS_Testing/
├── Framework/                # Core framework utilities and setup
│   ├── Core/                 # Core Python modules for testing
│   │   ├── Builder.py        # Handles build process
│   │   ├── Output_processer.py # Processes output logs
│   │   ├── Serial_connect.py # Manages serial connections
│   │   └── folder_manager.py # Manages test output directories
│   ├── Libraries/
│   │   └── requirments.txt   # Python dependencies
│   ├── Utils/
│   │   └── Makefile          # Automated setup and build commands
│   └── README.md             # Framework documentation

├── Tests/                    # Test case structure
│   ├── Inputs/               # Zephyr test source files
│   │   ├── TZR001/           # Test case TZR001
│   │   │   ├── src/main.c    # Zephyr application source
│   │   │   ├── CMakeLists.txt # CMake build config
│   │   │   ├── README.rst    # Test case description
│   │   │   ├── ZPT001.yaml   # Test metadata/configuration
│   │   │   └── prj.conf      # Zephyr-specific configurations
│   │   ├── TZR002/ ... TZR026/ # More test cases
│   ├── Outputs/              # Test results storage
│   │   ├── Output_files/     # Output files per test case
│   │   ├── logs/             # Logs for debugging
│   │   └── report/           # Test reports (HTML format)
│   └── Test_Scripts/         # Python test scripts
│       ├── TZR001.py ... TZR026.py  # Individual test scripts
│       ├── conftest.py       # pytest configuration
│       ├── pytest.ini        # pytest setup file
│       └── test_setup.py     # Test setup fixture

└── README.md                 # Overall project documentation

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

Add the following lines to `Zephyr_RTOS_Testing/Framework/Utils/zephyrproject/zephyr/Kconfig.zephyr`:

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

### Note:

The STM32F401re microcontroller board should be connected to the system to run tests in the running tests.

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
Outputs/                      
├── Output_files/             
│   ├── TZR001/               
│   │   ├── output.txt        
│   ├── TZR002/               
│   │   ├── output.txt        
│   ├── ...                   
│   ├── TZR026/               
│   │   ├── output.txt        
│
├── logs/                    
│   ├── TZR001.log            
│   ├── TZR002.log            
│   ├── ...                   
│   ├── TZR026.log            
│
└── reports/                   
    ├── assets/               
    │   ├── style.css       
    └──  ── Report.html
```
- **Logs** contain execution details.
- **Reports** provide an overview of test results.
- **Output** stores the raw outputs of the test scripts.

## OS Compatibility
This project was designed and tested on Ubuntu 22.04.5 LTS. Its compatibility with other operating systems is not guaranteed.

## Conclusion
This repository provides a fully automated setup and testing framework for Zephyr RTOS. By following the steps outlined above, you can set up the environment, modify configurations, run tests, and analyze results efficiently.
