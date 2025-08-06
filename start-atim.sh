#!/bin/bash

# Atim Assistant Startup Script
echo "🚀 Starting Atim Assistant..."

# Function to check if a port is in use
check_port() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to start backend
start_backend() {
    echo "📡 Starting Backend (Flask API)..."
    cd backend
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Install dependencies if needed
    if [ ! -f "requirements_installed" ]; then
        echo "Installing Python dependencies..."
        pip install -r requirements.txt
        touch requirements_installed
    fi
    
    # Start backend in background
    python app.py &
    BACKEND_PID=$!
    echo "Backend started with PID: $BACKEND_PID"
    cd ..
}

# Function to start frontend
start_frontend() {
    echo "🌐 Starting Frontend (React + Vite)..."
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing Node.js dependencies..."
        npm install
    fi
    
    # Start frontend in background
    npm run dev &
    FRONTEND_PID=$!
    echo "Frontend started with PID: $FRONTEND_PID"
}

# Function to stop services
stop_services() {
    echo "🛑 Stopping Atim Assistant..."
    pkill -f "python app.py" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    echo "Services stopped."
}

# Check if services are already running
if check_port 5070; then
    echo "⚠️  Backend is already running on port 5070"
else
    start_backend
fi

if check_port 5173; then
    echo "⚠️  Frontend is already running on port 5173"
else
    start_frontend
fi

# Wait a moment for services to start
sleep 3

# Check if services are running
echo ""
echo "🔍 Checking service status..."
if check_port 5070; then
    echo "✅ Backend API: http://localhost:5070"
else
    echo "❌ Backend failed to start"
fi

if check_port 5173; then
    echo "✅ Frontend: http://localhost:5173"
else
    echo "❌ Frontend failed to start"
fi

echo ""
echo "🎉 Atim Assistant is ready!"
echo "📱 Open your browser and visit: http://localhost:5173"
echo ""
echo "To stop the services, run: ./stop-atim.sh"
echo ""

# Save PIDs for later use
echo $BACKEND_PID > .backend.pid 2>/dev/null
echo $FRONTEND_PID > .frontend.pid 2>/dev/null 