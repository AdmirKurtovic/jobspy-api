#!/usr/bin/env python3.10
"""
JobSpy API Server for n8n Cloud Integration
Provides REST API endpoints to scrape jobs from various job boards
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
from datetime import datetime
import traceback
import logging
from typing import Optional, List, Dict, Any, Union

# Import JobSpy
from jobspy import scrape_jobs
from jobspy.model import Site, Country

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for n8n Cloud

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "jobspy-api"
    })

@app.route('/scrape-jobs', methods=['POST'])
def scrape_jobs_endpoint():
    """
    Main endpoint to scrape jobs
    Expected JSON payload:
    {
        "site_name": ["indeed", "linkedin", "glassdoor"],
        "search_term": "software engineer",
        "location": "San Francisco, CA",
        "results_wanted": 20,
        "country_indeed": "USA",
        "hours_old": 72,
        "is_remote": false,
        "job_type": "fulltime",
        "easy_apply": null,
        "linkedin_fetch_description": false,
        "description_format": "markdown",
        "proxies": null,
        "offset": 0
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract parameters with defaults
        site_name = data.get('site_name', ['indeed', 'linkedin'])
        search_term = data.get('search_term')
        location = data.get('location')
        results_wanted = data.get('results_wanted', 15)
        country_indeed = data.get('country_indeed', 'USA')
        hours_old = data.get('hours_old')
        is_remote = data.get('is_remote', False)
        job_type = data.get('job_type')
        easy_apply = data.get('easy_apply')
        linkedin_fetch_description = data.get('linkedin_fetch_description', False)
        description_format = data.get('description_format', 'markdown')
        proxies = data.get('proxies')
        offset = data.get('offset', 0)
        google_search_term = data.get('google_search_term')
        distance = data.get('distance', 50)
        linkedin_company_ids = data.get('linkedin_company_ids')
        enforce_annual_salary = data.get('enforce_annual_salary', False)
        verbose = data.get('verbose', 0)
        user_agent = data.get('user_agent')
        
        # Validate required parameters
        if not search_term:
            return jsonify({"error": "search_term is required"}), 400
        
        logger.info(f"Scraping jobs for: {search_term} in {location}")
        
        # Call JobSpy
        jobs_df = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            google_search_term=google_search_term,
            location=location,
            distance=distance,
            is_remote=is_remote,
            job_type=job_type,
            easy_apply=easy_apply,
            results_wanted=results_wanted,
            country_indeed=country_indeed,
            proxies=proxies,
            description_format=description_format,
            linkedin_fetch_description=linkedin_fetch_description,
            linkedin_company_ids=linkedin_company_ids,
            offset=offset,
            hours_old=hours_old,
            enforce_annual_salary=enforce_annual_salary,
            verbose=verbose,
            user_agent=user_agent
        )
        
        # Convert DataFrame to JSON-serializable format
        jobs_list = jobs_df.to_dict('records')
        
        # Clean up the data for JSON serialization
        for job in jobs_list:
            # Convert any non-serializable objects
            for key, value in job.items():
                if pd.isna(value):
                    job[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    job[key] = value.isoformat()
                elif hasattr(value, 'isoformat'):  # Handle other datetime-like objects
                    job[key] = value.isoformat()
        
        response = {
            "success": True,
            "total_jobs": len(jobs_list),
            "jobs": jobs_list,
            "metadata": {
                "search_term": search_term,
                "location": location,
                "sites_searched": site_name,
                "timestamp": datetime.now().isoformat(),
                "results_wanted": results_wanted,
                "actual_results": len(jobs_list)
            }
        }
        
        logger.info(f"Successfully scraped {len(jobs_list)} jobs")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error scraping jobs: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/sites', methods=['GET'])
def get_available_sites():
    """Get list of available job sites"""
    sites = [
        {"value": "indeed", "name": "Indeed"},
        {"value": "linkedin", "name": "LinkedIn"},
        {"value": "glassdoor", "name": "Glassdoor"},
        {"value": "google", "name": "Google Jobs"},
        {"value": "zip_recruiter", "name": "ZipRecruiter"},
        {"value": "bayt", "name": "Bayt"},
        {"value": "naukri", "name": "Naukri"},
        {"value": "bdjobs", "name": "BDJobs"}
    ]
    return jsonify({"sites": sites})

@app.route('/countries', methods=['GET'])
def get_available_countries():
    """Get list of available countries for Indeed"""
    countries = [
        {"value": "USA", "name": "United States"},
        {"value": "CANADA", "name": "Canada"},
        {"value": "UK", "name": "United Kingdom"},
        {"value": "AUSTRALIA", "name": "Australia"},
        {"value": "GERMANY", "name": "Germany"},
        {"value": "FRANCE", "name": "France"},
        {"value": "INDIA", "name": "India"},
        {"value": "SINGAPORE", "name": "Singapore"},
        {"value": "JAPAN", "name": "Japan"},
        {"value": "BRAZIL", "name": "Brazil"}
    ]
    return jsonify({"countries": countries})

@app.route('/job-types', methods=['GET'])
def get_job_types():
    """Get list of available job types"""
    job_types = [
        {"value": "fulltime", "name": "Full Time"},
        {"value": "parttime", "name": "Part Time"},
        {"value": "contract", "name": "Contract"},
        {"value": "internship", "name": "Internship"},
        {"value": "temporary", "name": "Temporary"}
    ]
    return jsonify({"job_types": job_types})

@app.route('/description-formats', methods=['GET'])
def get_description_formats():
    """Get list of available description formats"""
    formats = [
        {"value": "markdown", "name": "Markdown"},
        {"value": "html", "name": "HTML"},
        {"value": "plain", "name": "Plain Text"}
    ]
    return jsonify({"formats": formats})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
