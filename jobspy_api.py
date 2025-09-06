#!/usr/bin/env python3
"""
JobSpy API Server for Render Deployment
Includes job scraping functionality with mock data
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
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "jobspy-api",
        "message": "API is running successfully"
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
        
        location = data.get('location', '')
        results_wanted = data.get('results_wanted', 15)
        site_name = data.get('site_name', ['indeed', 'linkedin'])
        
        # Return mock job data
        mock_jobs = [
            {
                "title": f"Senior {search_term} Developer",
                "company": "TechCorp Inc",
                "location": location or "San Francisco, CA",
                "job_url": "https://example.com/job/1",
                "site": "indeed",
                "date_posted": "2024-01-15",
                "description": f"Join our team as a Senior {search_term} developer. We're looking for someone passionate about technology and innovation...",
                "salary": "$120,000 - $180,000",
                "job_type": "fulltime",
                "is_remote": True
            },
            {
                "title": f"{search_term} Engineer",
                "company": "StartupXYZ",
                "location": location or "New York, NY",
                "job_url": "https://example.com/job/2",
                "site": "linkedin",
                "date_posted": "2024-01-14",
                "description": f"Exciting opportunity for a {search_term} engineer to work on cutting-edge projects...",
                "salary": "$100,000 - $150,000",
                "job_type": "fulltime",
                "is_remote": False
            },
            {
                "title": f"Remote {search_term} Specialist",
                "company": "GlobalTech",
                "location": "Remote",
                "job_url": "https://example.com/job/3",
                "site": "glassdoor",
                "date_posted": "2024-01-13",
                "description": f"Fully remote position for a {search_term} specialist. Work from anywhere in the world...",
                "salary": "$90,000 - $130,000",
                "job_type": "fulltime",
                "is_remote": True
            },
            {
                "title": f"Lead {search_term} Architect",
                "company": "Enterprise Solutions",
                "location": location or "Austin, TX",
                "job_url": "https://example.com/job/4",
                "site": "indeed",
                "date_posted": "2024-01-12",
                "description": f"Lead {search_term} architect position with excellent growth opportunities...",
                "salary": "$140,000 - $200,000",
                "job_type": "fulltime",
                "is_remote": False
            },
            {
                "title": f"Junior {search_term} Developer",
                "company": "Learning Corp",
                "location": location or "Seattle, WA",
                "job_url": "https://example.com/job/5",
                "site": "linkedin",
                "date_posted": "2024-01-11",
                "description": f"Perfect entry-level position for aspiring {search_term} developers...",
                "salary": "$70,000 - $90,000",
                "job_type": "fulltime",
                "is_remote": True
            }
        ]
        
        # Limit results based on results_wanted
        limited_jobs = mock_jobs[:min(results_wanted, len(mock_jobs))]
        
        return jsonify({
            "message": f"Successfully scraped {len(limited_jobs)} jobs for '{search_term}'",
            "jobs": limited_jobs,
            "count": len(limited_jobs),
            "search_params": {
                "search_term": search_term,
                "location": location,
                "results_wanted": results_wanted,
                "site_name": site_name
            },
            "note": "This is mock data. For real job scraping, install JobSpy package."
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
    logger.info(f"Starting JobSpy API on port {port}")
    print(f"Starting JobSpy API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
