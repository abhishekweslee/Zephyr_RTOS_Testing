# Makefile for Automated Zephyr RTOS Setup

# Variables
ZEPHYR_DIR := ./zephyrproject
VENV_DIR := $(ZEPHYR_DIR)/.venv
PYTHON := python3
WEST := $(VENV_DIR)/bin/west
WEST2 := ./.venv/bin/west
WEST3 := ../.venv/bin/west

.PHONY: all setup_deps setup_zephyr install_sdk clean

all: setup_deps setup_zephyr install_sdk
	@echo "Zephyr RTOS environment setup completed successfully."

# Step 1: Install System Dependencies
setup_deps:
	sudo apt update && sudo apt upgrade -y
	sudo apt install --no-install-recommends -y \
		git cmake ninja-build gperf \
		ccache dfu-util device-tree-compiler wget \
		python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
		make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1 \
		python3-venv stlink-tools minicom
	cmake --version
	$(PYTHON) --version
	dtc --version

# Step 2: Set Up Zephyr Project
setup_zephyr: $(WEST)

$(VENV_DIR):
	@echo "Creating Python virtual environment..."
	sudo mkdir -p $(ZEPHYR_DIR) && sudo chmod 777 $(ZEPHYR_DIR)
	$(PYTHON) -m venv $(VENV_DIR)

$(WEST): $(VENV_DIR)
	@echo "Activating virtual environment and installing west..."
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip west
	$(VENV_DIR)/bin/west init $(ZEPHYR_DIR) && cd $(ZEPHYR_DIR)
	cd $(ZEPHYR_DIR) && $(WEST2) update
	cd $(ZEPHYR_DIR) && $(WEST2) zephyr-export
	cd $(ZEPHYR_DIR) && $(WEST2) packages pip --install

# Step 3: Install Zephyr SDK
install_sdk:
	@echo "Installing Zephyr SDK..."
	cd $(ZEPHYR_DIR)/zephyr && $(WEST3) sdk install
# Clean Up
clean:
	rm -rf $(ZEPHYR_DIR)
	@echo "Cleaned up Zephyr project directory."
