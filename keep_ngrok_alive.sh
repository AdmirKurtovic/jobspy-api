#!/bin/bash

# Keep ngrok alive script
# This script restarts ngrok if it goes down

API_URL="http://localhost:8000"
NGROK_PORT=8000

echo "🚀 Starting JobSpy API server..."
python3 api_server.py &
API_PID=$!

# Wait for API to start
sleep 5

echo "🌐 Starting ngrok tunnel..."
ngrok http $NGROK_PORT &
NGROK_PID=$!

# Function to check if ngrok is running
check_ngrok() {
    curl -s http://localhost:4040/api/tunnels > /dev/null 2>&1
    return $?
}

# Function to restart ngrok
restart_ngrok() {
    echo "🔄 Restarting ngrok..."
    kill $NGROK_PID 2>/dev/null
    sleep 2
    ngrok http $NGROK_PORT &
    NGROK_PID=$!
    sleep 3
}

# Keep checking and restart if needed
while true; do
    if ! check_ngrok; then
        echo "❌ ngrok tunnel down, restarting..."
        restart_ngrok
    else
        echo "✅ ngrok tunnel active"
    fi
    sleep 30
done

# Cleanup on exit
trap "kill $API_PID $NGROK_PID 2>/dev/null; exit" INT TERM
