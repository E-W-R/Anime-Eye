#!/bin/bash

# Check if the correct number of parameters is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <number_of_times> <python_script>"
    exit 1
fi

# Assign command-line arguments to variables
n="$1"
python_script="$2"

# Loop to call the Python script n times
for ((i=1; i<=n; i++)); do
    echo "Calling Python script: $python_script (Run $i)"
    python "$python_script"
done
