#!/bin/bash

# Atim Assistant Stop Script
echo "🛑 Stopping Atim Assistant..."

# Stop backend
echo "📡 Stopping Backend..."
pkill -f "python app.py" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend stopped"
else
    echo "ℹ️  Backend was not running"
fi

# Stop frontend
echo "🌐 Stopping Frontend..."
pkill -f "vite" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Frontend stopped"
else
    echo "ℹ️  Frontend was not running"
fi

# Clean up PID files
rm -f .backend.pid .frontend.pid 2>/dev/null

echo ""
echo "🎉 Atim Assistant has been stopped!"
echo "To start again, run: ./start-atim.sh" 