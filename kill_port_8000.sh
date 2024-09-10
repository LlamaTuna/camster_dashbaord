#!/bin/bash

# Find the process using port 8000
PID=$(sudo lsof -t -i:8005)

# Check if a process was found
if [ -z "$PID" ]; then
  echo "No process found on port 8005."
else
  # Kill the process using port 8000
  echo "Killing process on port 8000 (PID: $PID)"
  sudo kill -9 $PID
  echo "Process killed."
fi
