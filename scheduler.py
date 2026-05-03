# scheduler.py
import schedule
import time
import pandas as pd
from scraper.naukri_scraper import scrape_naukri
from analyzer.cleaner import clean_data
from utils.database import insert_jobs, get_recent_high_salary_jobs
from utils.emailer import send_high_salary_alert
from config import HIGH_SALARY_THRESHOLD

def run_pipeline():
    print("Starting daily scraping pipeline...")
    try:
        # 1. Scrape
        print("Scraping Naukri...")
        df_naukri = scrape_naukri()
        
        # Merge
        df_all =df_naukri

        if df_all.empty:
            print("No jobs scraped today.")
            return

        # 2. Clean
        print("Cleaning data...")
        df_clean = clean_data(df_all)
        
        # 3. Database Insertion
        print("Inserting into database...")
        insert_jobs(df_clean)
        
        # 4. High Salary Alert
        print("Checking for high salary jobs...")
        high_salary_jobs = get_recent_high_salary_jobs(HIGH_SALARY_THRESHOLD)
        if not high_salary_jobs.empty:
            print(f"Found {len(high_salary_jobs)} high salary jobs. Sending alert...")
            send_high_salary_alert(high_salary_jobs)
        else:
            print("No new high salary jobs found today.")
            
        print("Pipeline execution completed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    print("Scheduler started. Running initial pipeline execution...")
    run_pipeline()
    
    # Schedule every 24 hours
    schedule.every(24).hours.do(run_pipeline)
    
    print("Entering scheduling loop...")
    while True:
        schedule.run_pending()
        time.sleep(60)
