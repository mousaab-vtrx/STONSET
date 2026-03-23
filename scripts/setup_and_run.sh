#!/bin/bash
# Setup environments, DB, and launch app for manual testing
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND="$PROJECT_ROOT/backend"
FRONTEND="$PROJECT_ROOT/frontend"
VENV_NAME="venv"

echo "=========================================="
echo "  bdProject - Setup & Launch"
echo "=========================================="

# --- 1. Python environment ---
echo ""
echo "[1/6] Creating Python virtual environment..."
cd "$BACKEND"
if [ -d "$VENV_NAME" ]; then
    echo "  Venv exists at backend/$VENV_NAME"
else
    python3 -m venv "$VENV_NAME"
    echo "  Created backend/$VENV_NAME"
fi

echo "  Installing backend dependencies..."
source "$VENV_NAME/bin/activate"
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install pymysql -q
echo "  ✓ Backend dependencies installed"

# --- 2. Load .env ---
echo ""
echo "[2/6] Loading environment..."
cd "$BACKEND"
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "  Loaded .env"
else
    if [ -f ../.env.example ]; then
        echo "  No .env found. Copy .env.example to .env and set DATABASE_URL if needed."
    fi
fi

# --- 3. Database ---
echo ""
echo "[3/6] Database setup..."
cd "$PROJECT_ROOT"
source "$BACKEND/$VENV_NAME/bin/activate"
python scripts/create_db.py || true

echo "  Creating tables..."
python init_db.py

echo "  Seeding test data..."
cd "$BACKEND"
python -m app.db.seed_data
echo "  ✓ Database ready"

# --- 4. Frontend ---
echo ""
echo "[4/6] Installing frontend dependencies..."
cd "$FRONTEND"
npm install
echo "  ✓ Frontend dependencies installed"

# --- 5 & 6. Launch ---
echo ""
echo "[5/6] Starting backend..."
cd "$BACKEND"
source "$VENV_NAME/bin/activate"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
sleep 4

echo ""
echo "[6/6] Starting frontend..."
cd "$FRONTEND"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "  ✓ App is running!"
echo "=========================================="
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "  Frontend: http://localhost:5173"
echo ""
echo "  Test accounts (password: test1234):"
echo "    enseignant@test.com | chef@test.com | responsable@test.com"
echo ""
echo "  Press Ctrl+C to stop both servers."
echo "=========================================="

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
