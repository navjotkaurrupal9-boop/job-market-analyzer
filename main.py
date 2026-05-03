# main.py
from scraper.naukri_scraper import scrape_naukri
from analyzer.cleaner import clean_data
from analyzer.skills_analyzer import get_top_skills
from analyzer.salary_analyzer import avg_salary_by_location
from visualizer.charts import (
    plot_top_skills,
    plot_salary_by_location,
    plot_job_distribution
)

if __name__ == "__main__":
    print("=== Job Market Analyzer ===")

    print("Step 1: Scraping jobs...")
    raw_df = scrape_naukri()

    print("Step 2: Cleaning data...")
    clean_df = clean_data(raw_df)

    print("Step 3: Analyzing skills...")
    skills = get_top_skills(clean_df)
    print(skills)

    print("Step 4: Analyzing salaries...")
    salaries = avg_salary_by_location(clean_df)
    print(salaries)

    print("Step 5: Generating charts...")
    plot_top_skills(skills)
    plot_salary_by_location(salaries)
    plot_job_distribution(clean_df)

    print("Done! Check /reports folder for charts.")
