#!/usr/bin/env python3
"""
Railway-optimized JobSpy API Server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check requested")
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "jobspy-api-railway",
        "message": "API is running successfully",
        "port": os.environ.get('PORT', '8000')
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "JobSpy API Server",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "scrape_jobs": "/scrape-jobs",
            "sites": "/sites",
            "countries": "/countries",
            "job_types": "/job-types"
        }
    })

@app.route('/scrape-jobs', methods=['POST'])
def scrape_jobs_endpoint():
    try:
        data = request.get_json()
        logger.info(f"Scrape jobs request: {data}")
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        search_term = data.get('search_term')
        if not search_term:
            return jsonify({"error": "search_term is required"}), 400
        
        # Return mock data for testing
        mock_jobs = [
            {
                "title": f"Software Engineer - {search_term}",
                "company": "Tech Company Inc",
                "location": data.get('location', 'Remote'),
                "job_url": "https://example.com/job/1",
                "site": "indeed",
                "date_posted": "2024-01-15",
                "description": f"Looking for a {search_term} developer with experience in modern technologies...",
                "salary": "$80,000 - $120,000",
                "job_type": "fulltime",
                "is_remote": True
            },
            {
                "title": f"Senior {search_term} Developer",
                "company": "StartupXYZ",
                "location": data.get('location', 'San Francisco, CA'),
                "job_url": "https://example.com/job/2",
                "site": "linkedin",
                "date_posted": "2024-01-14",
                "description": f"Join our team as a Senior {search_term} developer. We're looking for someone passionate about technology...",
                "salary": "$100,000 - $150,000",
                "job_type": "fulltime",
                "is_remote": False
            },
            {
                "title": f"Remote {search_term} Engineer",
                "company": "GlobalTech",
                "location": "Remote",
                "job_url": "https://example.com/job/3",
                "site": "glassdoor",
                "date_posted": "2024-01-13",
                "description": f"Fully remote position for a {search_term} engineer. Work from anywhere in the world...",
                "salary": "$90,000 - $130,000",
                "job_type": "fulltime",
                "is_remote": True
            }
        ]
        
        return jsonify({
            "message": f"Mock data for '{search_term}' (JobSpy not available)",
            "jobs": mock_jobs,
            "count": len(mock_jobs),
            "search_params": {
                "search_term": search_term,
                "location": data.get('location', ''),
                "results_wanted": data.get('results_wanted', 15),
                "site_name": data.get('site_name', ['indeed', 'linkedin'])
            },
            "note": "This is mock data. Install JobSpy for real job scraping."
        })
        
    except Exception as e:
        logger.error(f"Error in scrape_jobs: {str(e)}")
        return jsonify({
            "error": f"Failed to process request: {str(e)}"
        }), 500

@app.route('/sites', methods=['GET'])
def get_sites():
    return jsonify({
        "sites": [
            "indeed", "linkedin", "glassdoor", "google", 
            "zip_recruiter", "bayt", "naukri", "bdjobs"
        ]
    })

@app.route('/countries', methods=['GET'])
def get_countries():
    return jsonify({
        "countries": [
            "USA", "CAN", "GBR", "AUS", "DEU", "FRA", "IND", "UAE"
        ]
    })

@app.route('/job-types', methods=['GET'])
def get_job_types():
    return jsonify({
        "job_types": [
            "fulltime", "parttime", "contract", "internship", "temporary"
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting server on port {port}")
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
