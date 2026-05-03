# analyzer/salary_analyzer.py
import pandas as pd

def avg_salary_by_location(df):
    df_clean = df.dropna(subset=["salary_min"])
    if df_clean.empty:
        return pd.DataFrame(columns=["Location", "Avg Salary (LPA)"])
    result = df_clean.groupby("location")["salary_min"].mean().sort_values(ascending=False).reset_index()

    result["Avg Salary (LPA)"] = result["salary_min"] / 100000.0
    result = result.drop(columns=["salary_min"])
    return result

def avg_salary_by_experience(df):
    df_clean = df.dropna(subset=["salary_min"])
    if df_clean.empty:
        return pd.DataFrame(columns=["Experience", "Avg Salary (LPA)"])
    result = (
        df_clean.groupby("experience")["salary_min"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    result["Avg Salary (LPA)"] = result["salary_min"] / 100000.0
    result = result.drop(columns=["salary_min"])
    return result

def top_hiring_companies(df, top_n=10):
    if df.empty:
        return pd.DataFrame(columns=["Company", "Number of Jobs"])
    result = df["company"].value_counts().head(top_n).reset_index()
    result.columns = ["Company", "Number of Jobs"]
    return result

def remote_vs_onsite_ratio(df):
    if df.empty or "job_type" not in df.columns:
        return pd.DataFrame(columns=["Job Type", "Count"])
    result = df["job_type"].value_counts().reset_index()
    result.columns = ["Job Type", "Count"]
    return result