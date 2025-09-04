#!/bin/bash
# JobSpy n8n Cloud Setup Script

echo "🚀 Setting up JobSpy API Server for n8n Cloud..."

# Check if Python 3.10 is installed
if ! command -v python3.10 &> /dev/null; then
    echo "❌ Python 3.10 not found. Installing..."
    brew install python@3.10
fi

# Install JobSpy and Flask
echo "📦 Installing dependencies..."
pip3.10 install python-jobspy flask flask-cors gunicorn

# Test the installation
echo "🧪 Testing JobSpy installation..."
python3.10 -c "from jobspy import scrape_jobs; print('✅ JobSpy installed successfully!')"

# Start the API server
echo "🌐 Starting API server on port 8000..."
echo "   API will be available at: http://localhost:8000"
echo "   Health check: http://localhost:8000/health"
echo "   Job scraping: http://localhost:8000/scrape-jobs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3.10 api_server.py
