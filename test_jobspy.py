#!/usr/bin/env python3
"""
Simple test to check if JobSpy works
"""

try:
    print("Testing JobSpy import...")
    from jobspy import scrape_jobs
    print("✅ JobSpy imported successfully!")
    
    print("Testing basic job scraping...")
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term="software engineer",
        location="San Francisco, CA",
        results_wanted=2
    )
    
    print(f"✅ Successfully scraped {len(jobs)} jobs!")
    print("Sample job:")
    if len(jobs) > 0:
        print(f"  Title: {jobs.iloc[0]['title']}")
        print(f"  Company: {jobs.iloc[0].get('company_name', 'N/A')}")
        print(f"  Location: {jobs.iloc[0].get('location', 'N/A')}")
        print(f"  Available columns: {list(jobs.columns)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
