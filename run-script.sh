#!/bin/bash

# Recipe Management System - Full Stack Run Script
# This script sets up and runs both backend (Django) and frontend (React) servers.
# Run from the project root: ./run-script.sh

set -e

# --- Prerequisite Checks ---
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python3 is required but not installed. Aborting."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo >&2 "pip3 is required but not installed. Aborting."; exit 1; }
command -v node >/dev/null 2>&1 || { echo >&2 "Node.js is required but not installed. Aborting."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo >&2 "npm is required but not installed. Aborting."; exit 1; }

# --- Backend Setup ---
echo "\n=== Setting up Backend ==="
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations recipes
python manage.py migrate

# Seed data (optional, safe to run multiple times)
echo "Seeding initial data..."
python manage.py seed_data

echo "If this is your first time, you should create a superuser:"
echo "  cd backend && source .venv/bin/activate && python manage.py createsuperuser"
echo "(This step is interactive and must be done manually if you haven't already.)"

# Start backend server in background
echo "Starting backend server on http://127.0.0.1:8000 ..."
nohup python manage.py runserver > ../backend-server.log 2>&1 &
BACKEND_PID=$!
cd ..

# --- Frontend Setup ---
echo "\n=== Setting up Frontend ==="
cd frontend

# Install npm dependencies
npm install

# Start frontend server in background
echo "Starting frontend server on http://localhost:3000 ..."
npm start > ../frontend-server.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "\n=== All Done! ==="
echo "Backend running at: http://127.0.0.1:8000"
echo "Frontend running at: http://localhost:3000"
echo "Logs: backend-server.log, frontend-server.log"
echo "To stop servers: kill $BACKEND_PID $FRONTEND_PID"
