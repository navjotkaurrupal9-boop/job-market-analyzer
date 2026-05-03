# visualizer/charts.py
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from wordcloud import WordCloud

os.makedirs("reports", exist_ok=True)

def plot_top_skills(skills_df):
    if skills_df.empty:
        return None
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=skills_df, x="Count", y="Skill", palette="viridis", ax=ax,hue="Skill")
    ax.set_title("Top In-Demand Skills", fontsize=16)
    plt.tight_layout()
    fig.savefig("reports/top_skills.png")
    return fig

def plot_salary_by_location(salary_df):
    if salary_df.empty:
        return None
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=salary_df.head(10), x="Avg Salary (LPA)", y="location", palette="coolwarm", ax=ax,hue="location")
    ax.set_title("Average Salary by Location", fontsize=16)
    plt.tight_layout()
    fig.savefig("reports/salary_by_location.png")
    return fig

def plot_job_distribution(df):
    if df.empty or "location" not in df.columns: return None
    location_counts = df["location"].value_counts().head(8)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(location_counts, labels=location_counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Job Distribution by City")
    plt.tight_layout()
    fig.savefig("reports/location_pie.png")
    return fig


def plot_trend_line(df):
    if df.empty or "timestamp" not in df.columns:
        return None
    df_copy = df.copy()
    try:
        df_copy["date"] = pd.to_datetime(df_copy["timestamp"], errors="coerce").dt.date
        df_copy = df_copy.dropna(subset=["date"])

        if df_copy["date"].nunique() < 2:
            # Not enough different dates — show bar chart instead
            trend = df_copy.groupby("date").size().reset_index(name="Count")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(trend["date"].astype(str), trend["Count"], color="steelblue")
            ax.set_title("Job Postings by Date", fontsize=16)
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Jobs")
            plt.xticks(rotation=45)
            plt.tight_layout()
            fig.savefig("reports/trend_line.png")
            return fig

        trend = df_copy.groupby("date").size().reset_index(name="Count")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=trend, x="date", y="Count", marker="o", ax=ax)
        ax.set_title("Job Postings Over Time", fontsize=16)
        ax.set_xlabel("Date Posted")
        ax.set_ylabel("Number of Jobs")
        plt.xticks(rotation=45)
        plt.tight_layout()
        fig.savefig("reports/trend_line.png")
        return fig
    except Exception as e:
        print(f"Error plotting trend line: {e}")
        return None

def plot_experience_salary_box(df):
    if df.empty or "salary_min" not in df.columns or "experience" not in df.columns: return None
    df_clean = df.copy().dropna(subset=["salary_min", "experience"])
    # filter out bad exp strings if necessary, though boxplot handles categories
    if df_clean.empty: return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    df_clean["salary_lpa"] = df_clean["salary_min"] / 100000.0
    sns.boxplot(data=df_clean, x="experience", y="salary_lpa", palette="Set2", ax=ax,hue="experience")
    ax.set_title("Salary Distribution by Experience", fontsize=16)
    ax.set_ylabel("Salary (LPA)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig("reports/experience_box.png")
    return fig

def plot_word_cloud(df):
    if df.empty or "title" not in df.columns: return None
    text = " ".join(df["title"].astype(str).tolist())
    if not text.strip(): return None
    
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Job Titles Word Cloud", fontsize=16)
    plt.tight_layout()
    fig.savefig("reports/word_cloud.png")
    return fig

def plot_top_hiring_companies(companies_df):
    if companies_df.empty:
        return None
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=companies_df, x="Number of Jobs", y="Company", palette="Blues_d", ax=ax)
    ax.set_title("Top Hiring Companies", fontsize=16)
    plt.tight_layout()
    fig.savefig("reports/top_companies.png")
    return fig

def plot_remote_vs_onsite(ratio_df):
    if ratio_df.empty:
        return None
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(ratio_df["Count"], labels=ratio_df["Job Type"], autopct="%1.1f%%", startangle=90,
           colors=["#4CAF50", "#2196F3", "#FF9800"])
    ax.set_title("Remote vs Hybrid vs On-site", fontsize=16)
    plt.tight_layout()
    fig.savefig("reports/remote_onsite.png")
    return fig