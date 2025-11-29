#!/bin/bash

# --- 1. CONFIGURATION ---
VENV_PATH="/home/wlsbase/git_repo_social_post/sp_venv"
APP_PATH="/home/wlsbase/git_repo_social_post/src/app.py"

# --- 2. ERROR CHECKING & DEBUGGING ---

# Set e: Exit immediately if a command exits with a non-zero status.
# Set x: Print commands and their arguments as they are executed (for logging).
set -xe 

# --- 2.5 Random Delay Configuration ---

# Define the maximum number of minutes to wait (e.g., 60 minutes for a 1-hour window)
MAX_DELAY_MINUTES=1 

# Calculate a random number of seconds between 0 and (MAX_DELAY_MINUTES * 60)
RANDOM_SECONDS=$(( RANDOM % (MAX_DELAY_MINUTES * 60) ))

# --- Script Execution ---

echo "Starting cron job shell at $(date)"
echo "Delaying execution for $RANDOM_SECONDS seconds to ensure non-identical run time..."

# --- Apply the random delay
sleep $RANDOM_SECONDS

echo "Resuming execution at $(date)"

echo "--- Starting Social Post Application ---"

# --- 3. VIRTUAL ENVIRONMENT ACTIVATION ---

# Check if the venv path exists before trying to source it
if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH. Exiting."
    exit 1
fi

echo "Activating virtual environment..."
# Source the activate script
source "$VENV_PATH/bin/activate"

# Check the Python being used (VERIFICATION STEP)
echo "Python interpreter verified:"
which python

# --- 4. EXECUTION ---

echo "Running application script..."
# Run the Python script using the python from the activated venv
# Note: We can simplify the call now since 'python' is in the PATH
python "$APP_PATH"

# --- 5. CLEANUP ---

echo "Deactivating virtual environment..."
deactivate

echo "--- Script Finished Successfully ---"
