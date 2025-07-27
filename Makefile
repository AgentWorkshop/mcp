# Makefile for MCP Python Examples

.PHONY: help setup install setup-env run-weather-server run-weather-client run-remote-server run-remote-client

help:
	@echo "Available commands:"
	@echo "  setup              - Create a Python virtual environment and install dependencies"
	@echo "  install            - Install Python dependencies from requirements.txt"
	@echo "  setup-env          - Guide to create .env file from .env.example"
	@echo "  run-weather-server - Run the standalone weather tool server"
	@echo "  run-weather-client - Run the GenAI agent client for the weather server"
	@echo "  run-remote-server  - Run the authenticated FastAPI server"
	@echo "  run-remote-client  - Run the client for the authenticated server (requires MCP_CLIENT_TOKEN)"

setup: venv/bin/activate
	@./venv/bin/pip install -r requirements.txt
	@echo "\nSetup complete. Activate the virtual environment with:\nsource venv/bin/activate"

venv/bin/activate:
	@if [ ! -d "venv" ]; then \
		echo "Creating Python virtual environment in 'venv'..."; \
		python3 -m venv venv; \
	fi

install:
	pip install -r requirements.txt

# This target provides instructions for setting up the environment file.
setup-env:
	@echo "Please copy the '.env.example' file to a new file named '.env'."
	@echo "Then, open '.env' and add your GENAI_API_KEY."

run-weather-server:
	python example/server/weather.py

run-weather-client:
	python example/client/client.py

run-remote-server:
	python main_remote.py

# The client script (client_remote.py) already checks for the MCP_CLIENT_TOKEN environment variable.
run-remote-client:
	python client_remote.py