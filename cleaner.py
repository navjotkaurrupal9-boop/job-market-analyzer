# analyzer/cleaner.py
import pandas as pd
import re
import os
from config import CLEAN_DATA_PATH

def clean_data(df):
    if df.empty:
        return df

    # Drop duplicates
    df = df.drop_duplicates(subset=["title", "company", "location"])

    # Drop rows with no title or company
    df = df.dropna(subset=["title", "company"])

    # Clean text columns
    df["title"]    = df["title"].astype(str).str.strip().str.lower()
    df["company"]  = df["company"].astype(str).str.strip()
    df["location"] = df["location"].astype(str).str.strip()

    # Make sure new fields exist
    if "job_type" not in df.columns:
        df["job_type"] = "On-site"
    if "source_url" not in df.columns:
        df["source_url"] = "WILL BW AVAILABLE"
    if "timestamp" not in df.columns:
        from datetime import datetime
        df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Clean job type explicitly
    def standardize_job_type(row):
        loc = row.get("location", "").lower()
        jt = str(row.get("job_type", "")).lower()
        if "remote" in loc or "remote" in jt:
            return "Remote"
        elif "hybrid" in loc or "hybrid" in jt:
            return "Hybrid"
        return "On-site"
        
    df["job_type"] = df.apply(standardize_job_type, axis=1)

    # Extract salary numbers
    df["salary_min"], df["salary_max"] = zip(*df["salary"].astype(str).apply(extract_salary))

    # Clean skills — split by comma into list
    df["skills_list"] = df["skills"].astype(str).apply(
        lambda x: [s.strip().lower() for s in x.split(",")] if x != "Not listed" and x != "nan" else []
    )

    os.makedirs(os.path.dirname(CLEAN_DATA_PATH), exist_ok=True)
    df.to_csv(CLEAN_DATA_PATH, index=False)
    return df

def extract_salary(salary_text):
    """Extract min and max salary from text like '5-8 Lacs' or '1,50,000'"""
    salary_text_lower = salary_text.lower().replace(',', '')
    numbers = re.findall(r'\d+\.?\d*', salary_text_lower)
    
    multiplier = 100000 if 'lac' in salary_text_lower or 'lakh' in salary_text_lower else 1
    
    if len(numbers) >= 2:
        return float(numbers[0]) * multiplier, float(numbers[1]) * multiplier
    elif len(numbers) == 1:
        return float(numbers[0]) * multiplier, float(numbers[0]) * multiplier
    return None, None