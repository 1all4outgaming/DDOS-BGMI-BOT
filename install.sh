#!/bin/bash

# Prompt user for the Python file to run
read -p "Enter the name of the Python file to run (without .py extension): " python_file

# Check if the requirements.txt file exists
if [ -f requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "No requirements.txt file found. Skipping dependency installation."
fi

# Check if the specified Python file exists
if [ -f "${python_file}.py" ]; then
    echo "Running ${python_file}.py..."
    python3 "${python_file}.py"
else
    echo "Error: ${python_file}.py does not exist."
fi
