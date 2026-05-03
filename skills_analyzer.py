
# analyzer/skills_analyzer.py
from collections import Counter
import pandas as pd
from config import SKILLS_LIST

def analyze_skills(df):
    # Flatten all skills into one list
    all_skills = []
    for skills in df["skills_list"]:
        all_skills.extend(skills)

    # Count frequency
    skill_counts = Counter(all_skills)

    # Filter only tracked skills
    tracked = {
        skill: skill_counts[skill]
        for skill in SKILLS_LIST
        if skill in skill_counts
    }

    result_df = pd.DataFrame(
        tracked.items(),
        columns=["Skill", "Count"]
    ).sort_values("Count", ascending=False)

    return result_df

def get_top_skills(df, top_n=10):
    return analyze_skills(df).head(top_n)