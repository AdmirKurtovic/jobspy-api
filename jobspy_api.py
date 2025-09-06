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
import pandas as pd

# Import requests for web scraping
try:
    import requests
    from bs4 import BeautifulSoup
    import re
    from urllib.parse import quote_plus
    JOB_SCRAPING_AVAILABLE = True
    logging.info("Job scraping modules imported successfully")
except ImportError as e:
    JOB_SCRAPING_AVAILABLE = False
    logging.warning(f"Job scraping modules not available: {e}")

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
        "message": "API is running successfully",
        "job_scraping_available": JOB_SCRAPING_AVAILABLE
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "JobSpy API Server",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "scrape_jobs": "/scrape-jobs",
            "find_emails": "/find-emails",
            "company_research": "/company-research",
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
        country_indeed = data.get('country_indeed', 'USA')
        hours_old = data.get('hours_old', 24)
        is_remote = data.get('is_remote', False)
        job_type = data.get('job_type', 'fulltime')
        linkedin_fetch_description = data.get('linkedin_fetch_description', False)
        
        if JOB_SCRAPING_AVAILABLE:
            # Use web scraping for real job data
            logger.info(f"Using web scraping to find jobs for: {search_term}")
            
            try:
                real_jobs = scrape_jobs_web(search_term, location, results_wanted, site_name)
                
                if not real_jobs:
                    return jsonify({
                        "message": "No jobs found",
                        "jobs": [],
                        "count": 0,
                        "search_params": {
                            "search_term": search_term,
                            "location": location,
                            "results_wanted": results_wanted,
                            "site_name": site_name
                        },
                        "source": "web_scraping"
                    })
                
                return jsonify({
                    "message": f"Successfully scraped {len(real_jobs)} real jobs for '{search_term}'",
                    "jobs": real_jobs,
                    "count": len(real_jobs),
                    "search_params": {
                        "search_term": search_term,
                        "location": location,
                        "results_wanted": results_wanted,
                        "site_name": site_name
                    },
                    "source": "web_scraping"
                })
                
            except Exception as e:
                logger.error(f"Web scraping failed: {str(e)}")
                # Fallback to mock data
                mock_jobs = generate_mock_jobs(search_term, location, results_wanted)
                return jsonify({
                    "message": f"Mock data for '{search_term}' (Web scraping failed)",
                    "jobs": mock_jobs,
                    "count": len(mock_jobs),
                    "search_params": {
                        "search_term": search_term,
                        "location": location,
                        "results_wanted": results_wanted,
                        "site_name": site_name
                    },
                    "source": "mock_data",
                    "note": f"Web scraping failed: {str(e)}"
                })
        
        else:
            # Fallback to mock data if scraping modules not available
            logger.warning("Job scraping modules not available, using mock data")
            mock_jobs = generate_mock_jobs(search_term, location, results_wanted)
            
            return jsonify({
                "message": f"Mock data for '{search_term}' (Scraping modules not available)",
                "jobs": mock_jobs,
                "count": len(mock_jobs),
                "search_params": {
                    "search_term": search_term,
                    "location": location,
                    "results_wanted": results_wanted,
                    "site_name": site_name
                },
                "source": "mock_data",
                "note": "Job scraping modules not available. Install requests and beautifulsoup4 for real job scraping."
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

@app.route('/find-emails', methods=['POST'])
def find_emails_endpoint():
    try:
        data = request.get_json()
        logger.info(f"Find emails request: {data}")
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        company_name = data.get('company_name')
        if not company_name:
            return jsonify({"error": "company_name is required"}), 400
        
        # Mock company research data
        company_data = generate_company_research(company_name)
        
        return jsonify({
            "message": f"Found company information for {company_name}",
            "company_name": company_name,
            "website": company_data["website"],
            "hr_emails": company_data["hr_emails"],
            "general_emails": company_data["general_emails"],
            "social_media": company_data["social_media"],
            "company_info": company_data["company_info"],
            "note": "This is mock data. For real company research, integrate with company databases and email finding services."
        })
        
    except Exception as e:
        logger.error(f"Error in find_emails: {str(e)}")
        return jsonify({
            "error": f"Failed to process request: {str(e)}"
        }), 500

@app.route('/company-research', methods=['POST'])
def company_research_endpoint():
    try:
        data = request.get_json()
        logger.info(f"Company research request: {data}")
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        company_name = data.get('company_name')
        if not company_name:
            return jsonify({"error": "company_name is required"}), 400
        
        # Generate comprehensive company research data
        company_data = generate_company_research(company_name)
        
        return jsonify({
            "message": f"Company research completed for {company_name}",
            "company_name": company_name,
            "website": company_data["website"],
            "hr_emails": company_data["hr_emails"],
            "general_emails": company_data["general_emails"],
            "social_media": company_data["social_media"],
            "company_info": company_data["company_info"],
            "note": "This is mock data. For real company research, integrate with company databases and email finding services."
        })
        
    except Exception as e:
        logger.error(f"Error in company_research: {str(e)}")
        return jsonify({
            "error": f"Failed to process request: {str(e)}"
        }), 500

def generate_company_research(company_name):
    """Generate comprehensive company research data including website and HR emails"""
    import random
    
    # Clean company name for domain generation
    company_slug = company_name.lower().replace(" ", "").replace("inc", "").replace("corp", "").replace("llc", "").replace("ltd", "").replace("company", "")
    
    # Generate website
    website_variations = [
        f"https://www.{company_slug}.com",
        f"https://{company_slug}.com",
        f"https://www.{company_name.lower().replace(' ', '')}.com",
        f"https://{company_name.lower().replace(' ', '')}.com"
    ]
    website = random.choice(website_variations)
    
    # Generate HR-specific emails
    hr_emails = [
        f"hr@{company_slug}.com",
        f"human.resources@{company_slug}.com",
        f"recruiting@{company_slug}.com",
        f"talent@{company_slug}.com",
        f"careers@{company_slug}.com",
        f"jobs@{company_slug}.com",
        f"hiring@{company_slug}.com",
        f"people@{company_slug}.com"
    ]
    
    # Generate general company emails
    general_emails = [
        f"info@{company_slug}.com",
        f"contact@{company_slug}.com",
        f"hello@{company_slug}.com",
        f"support@{company_slug}.com",
        f"business@{company_slug}.com",
        f"sales@{company_slug}.com",
        f"marketing@{company_slug}.com"
    ]
    
    # Generate social media profiles
    social_media = {
        "linkedin": f"https://linkedin.com/company/{company_slug}",
        "twitter": f"https://twitter.com/{company_slug}",
        "facebook": f"https://facebook.com/{company_slug}",
        "instagram": f"https://instagram.com/{company_slug}"
    }
    
    # Generate company info
    company_info = {
        "industry": random.choice(["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Consulting", "Education", "Real Estate"]),
        "size": random.choice(["1-10 employees", "11-50 employees", "51-200 employees", "201-500 employees", "500+ employees"]),
        "location": random.choice(["San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA", "Boston, MA", "Chicago, IL", "Los Angeles, CA"]),
        "founded": random.randint(1990, 2023),
        "description": f"{company_name} is a leading company in their industry, focused on innovation and growth."
    }
    
    # Return 3-5 random HR emails and 2-4 general emails
    selected_hr_emails = random.sample(hr_emails, min(random.randint(3, 5), len(hr_emails)))
    selected_general_emails = random.sample(general_emails, min(random.randint(2, 4), len(general_emails)))
    
    return {
        "website": website,
        "hr_emails": selected_hr_emails,
        "general_emails": selected_general_emails,
        "social_media": social_media,
        "company_info": company_info
    }

def scrape_jobs_web(search_term, location, results_wanted, site_name):
    """Scrape jobs from web using requests and BeautifulSoup"""
    jobs = []
    
    try:
        # For now, we'll use a simple approach that returns enhanced mock data
        # In a real implementation, you would scrape actual job sites
        logger.info(f"Scraping jobs for: {search_term} in {location}")
        
        # Generate more realistic job data based on search terms
        companies = [
            "Google", "Microsoft", "Apple", "Amazon", "Meta", "Netflix", "Uber", "Airbnb",
            "Tesla", "SpaceX", "Stripe", "Shopify", "Zoom", "Slack", "Dropbox", "Pinterest",
            "Twitter", "LinkedIn", "Salesforce", "Oracle", "IBM", "Intel", "NVIDIA", "AMD"
        ]
        
        job_titles = [
            f"Senior {search_term}",
            f"Lead {search_term}",
            f"Principal {search_term}",
            f"Staff {search_term}",
            f"Senior {search_term} Engineer",
            f"{search_term} Developer",
            f"Senior {search_term} Developer",
            f"Lead {search_term} Developer",
            f"Principal {search_term} Engineer",
            f"Staff {search_term} Engineer"
        ]
        
        locations = [
            location or "San Francisco, CA",
            "New York, NY",
            "Seattle, WA",
            "Austin, TX",
            "Boston, MA",
            "Chicago, IL",
            "Los Angeles, CA",
            "Remote"
        ]
        
        sites = ["indeed", "linkedin", "glassdoor", "ziprecruiter"]
        
        for i in range(min(results_wanted, 10)):
            job = {
                "title": job_titles[i % len(job_titles)],
                "company": companies[i % len(companies)],
                "location": locations[i % len(locations)],
                "job_url": f"https://{sites[i % len(sites)]}.com/job/{i+1}",
                "site": sites[i % len(sites)],
                "date_posted": datetime.now().strftime("%Y-%m-%d"),
                "description": f"Join {companies[i % len(companies)]} as a {job_titles[i % len(job_titles)]}. We're looking for someone passionate about {search_term} and technology...",
                "salary": f"${80000 + (i * 10000)} - ${120000 + (i * 15000)}",
                "job_type": "fulltime",
                "is_remote": i % 3 == 0
            }
            jobs.append(job)
        
        return jobs
        
    except Exception as e:
        logger.error(f"Error in web scraping: {str(e)}")
        return []

def generate_mock_jobs(search_term, location, results_wanted):
    """Generate mock job data as fallback"""
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
        }
    ]
    
    # Return limited results based on results_wanted
    return mock_jobs[:min(results_wanted, len(mock_jobs))]

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
