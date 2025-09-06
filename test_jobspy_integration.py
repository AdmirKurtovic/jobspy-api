#!/usr/bin/env python3
"""
Test script for JobSpy integration
"""

import requests
import json

# Test the deployed API
API_URL = "https://jobspy-api-jlyc.onrender.com"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_job_scraping():
    """Test job scraping with real JobSpy"""
    print("🔍 Testing job scraping...")
    
    payload = {
        "search_term": "software engineer",
        "location": "San Francisco, CA",
        "results_wanted": 5,
        "site_name": ["indeed", "linkedin"]
    }
    
    response = requests.post(
        f"{API_URL}/scrape-jobs",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Message: {data.get('message', 'No message')}")
    print(f"Source: {data.get('source', 'Unknown')}")
    print(f"Jobs found: {data.get('count', 0)}")
    
    if data.get('jobs'):
        print("\nFirst job:")
        first_job = data['jobs'][0]
        print(f"  Title: {first_job.get('title', 'N/A')}")
        print(f"  Company: {first_job.get('company', 'N/A')}")
        print(f"  Location: {first_job.get('location', 'N/A')}")
        print(f"  Site: {first_job.get('site', 'N/A')}")
        print(f"  URL: {first_job.get('job_url', 'N/A')}")
    print()

def test_company_research():
    """Test company research"""
    print("🔍 Testing company research...")
    
    payload = {
        "company_name": "Google"
    }
    
    response = requests.post(
        f"{API_URL}/company-research",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Message: {data.get('message', 'No message')}")
    print(f"Company: {data.get('company_name', 'N/A')}")
    print(f"Website: {data.get('website', 'N/A')}")
    print(f"HR Emails: {data.get('hr_emails', [])}")
    print()

if __name__ == "__main__":
    print("🚀 Testing JobSpy API Integration")
    print("=" * 50)
    
    test_health()
    test_job_scraping()
    test_company_research()
    
    print("✅ Testing completed!")
