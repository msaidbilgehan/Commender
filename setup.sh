#!/bin/bash

# Define the path to the virtual environment
VENV_DIR="venv"

# Step 1: Create a virtual environment if it does not exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m virtualenv $VENV_DIR
fi

# Step 2: Activate the virtual environment
source $VENV_DIR/bin/activate

# Step 3: Install dependencies from requirements.txt
pip install -r requirements.txt

# Step 4: Add the project start command to crontab
(crontab -l 2>/dev/null; echo "@reboot $(pwd)/$VENV_DIR/bin/python $(pwd)/app.py &") | crontab -

# Step 5: Start the app in the background
nohup python app.py &

echo "Setup and execution completed."
