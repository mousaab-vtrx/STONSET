#!/bin/bash
# Start backend with proper binding for WSL/Windows interop

cd /mnt/d/bdProject/backend

# Activate virtual environment
source newenv/bin/activate

# Start uvicorn on 0.0.0.0 to be accessible from Windows
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
