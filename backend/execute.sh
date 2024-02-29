#!/bin/bash

# Run kill.py in a new terminal
mate-terminal --title="kill.py" --command="python3 kill.py" &

# Run monitor_sys.py in a new terminal
mate-terminal --title="monitor_sys.py" --command="python3 monitor_sys.py" &

# Run fetch_process.py in a new terminal
mate-terminal --title="fetch_process.py" --command="python3 fetch_process.py" &
