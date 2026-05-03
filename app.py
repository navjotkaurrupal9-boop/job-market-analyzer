# app.py
import streamlit as st
import pandas as pd
from scraper.naukri_scraper import scrape_naukri
from analyzer.cleaner import clean_data
from analyzer.skills_analyzer import get_top_skills
from analyzer.salary_analyzer import avg_salary_by_location,top_hiring_companies,remote_vs_onsite_ratio
from visualizer.charts import (
    plot_top_skills, plot_salary_by_location, plot_job_distribution,
    plot_trend_line, plot_experience_salary_box, plot_word_cloud,
    plot_top_hiring_companies, plot_remote_vs_onsite
)
import io
import os
import config

st.set_page_config(page_title="Job Market Analyzer", layout="wide")
st.title("🧑‍💼 Job Market Analyzer")

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.header("🔧 Configuration")
if st.sidebar.button("🗑️ Clear Data", key="clear"):
    st.session_state.clear()
    st.rerun()
# Role and Location inputs (used by scraper)
role     = st.sidebar.text_input("Job Role", "")
location = st.sidebar.text_input("Location", "")

st.sidebar.markdown("---")

# ── Option 1: Live Scraping ───────────────────────────────────────────────────
st.sidebar.subheader("🌐 Live Scraping")
if st.sidebar.button("🔍 Scrape Jobs Now"):
    st.session_state.clear()
    config.SEARCH_ROLE = role
    config.SEARCH_LOCATION = location
    with st.spinner(f"Scraping {role} jobs in {location} from Naukri..."):
        try:
            df1 = scrape_naukri()
            if df1.empty:
                st.warning("⚠️ No jobs scraped. Naukri may have blocked the request. Try loading saved data instead.")
            else:
                df_clean = clean_data(df1)
                st.session_state["df"] = df_clean
                st.session_state["source"] = "scraped"
                st.success(f"✅ Scraped and cleaned {len(df_clean)} jobs for '{role}' in '{location}'!")
                st.rerun()
        except Exception as e:
            st.error(f"Scraping failed: {e}")

st.sidebar.markdown("---")

# ── Option 2: Load Saved CSV ──────────────────────────────────────────────────
st.sidebar.subheader("📂 Load Saved Data")

# Filter inputs for saved data
role_filter     = st.sidebar.text_input("Filter by Role (optional)", "")
location_filter = st.sidebar.text_input("Filter by Location (optional)", "")

if st.sidebar.button("📂 Load Saved Data"):
    st.session_state.clear()
    csv_path = "data/processed/job_clean.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        # Apply role filter
        if role_filter.strip():
            df = df[df["title"].astype(str).str.contains(role_filter.strip(), case=False, na=False)]

        # Apply location filter
        if location_filter.strip():
            df = df[df["location"].astype(str).str.contains(location_filter.strip(), case=False, na=False)]

        if df.empty:
            st.warning(f"⚠️ No jobs found for role='{role_filter}' in location='{location_filter}'. Try different filters.")
        else:
            st.session_state["df"] = df
            st.rerun()
            st.session_state["source"] = "csv"
            st.success(f"✅ Loaded {len(df)} jobs from saved dataset!")
    else:
        st.error("❌ No saved data found at data/processed/job_clean.csv. Please scrape first or check the file path.")

st.sidebar.markdown("---")

# ── Option 3: Upload CSV manually ────────────────────────────────────────────
st.sidebar.subheader("⬆️ Upload CSV")
uploaded = st.sidebar.file_uploader("Upload your own CSV file", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    st.session_state["df"] = df

    st.session_state["source"] = "uploaded"
    st.success(f"✅ Loaded {len(df)} jobs from uploaded file!")
    st.rerun()

# ── Main Dashboard ────────────────────────────────────────────────────────────
if "df" in st.session_state:
    df = st.session_state["df"]

    # Show data source info
    source = st.session_state.get("source", "")
    if source == "scraped":
        st.info("📡 Showing live scraped data")
    elif source == "csv":
        st.info("💾 Showing saved dataset")
    elif source == "uploaded":
        st.info("📁 Showing uploaded CSV data")

    # ── KPI Metrics ───────────────────────────────────────────────────────────
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Jobs Found", len(df))
    col2.metric("Companies Hiring", df["company"].nunique())
    col3.metric("Cities Covered", df["location"].nunique())

    avg_sal = 0
    if "salary_min" in df.columns:
        valid_sal = df["salary_min"].dropna()
        if not valid_sal.empty:
            avg_sal = valid_sal.mean() / 100000.0
    col4.metric("Avg Salary (LPA)", f"₹{avg_sal:.1f}L")

    st.markdown("---")

    # ── Charts Row 1 ──────────────────────────────────────────────────────────
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("🔥 Top Skills")
        try:
            # Make sure skills_list column exists
            if "skills_list" not in df.columns:
                df["skills_list"] = df["skills"].astype(str).apply(
                    lambda x: [s.strip().lower() for s in x.split(",") if s.strip()]
                    if x not in ["Not listed", "nan", ""] else []
                )
            fig1 = plot_top_skills(get_top_skills(df))
            if fig1:
                st.pyplot(fig1)
            else:
                st.info("Not enough skill data to display chart.")
        except Exception as e:
            st.warning(f"Could not render skills chart: {e}")

    with row1_col2:
        st.subheader("💰 Salary by Location")
        try:
            fig2 = plot_salary_by_location(avg_salary_by_location(df))
            if fig2:
                st.pyplot(fig2)
            else:
                st.info("Not enough salary data to display chart.")
        except Exception as e:
            st.warning(f"Could not render salary chart: {e}")

    # ── Charts Row 2 ──────────────────────────────────────────────────────────
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("🌍 Job Distribution by City")
        try:
            fig3 = plot_job_distribution(df)
            if fig3:
                st.pyplot(fig3)
            else:
                st.info("Not enough location data to display chart.")
        except Exception as e:
            st.warning(f"Could not render distribution chart: {e}")

    with row2_col2:
        st.subheader("📈 Job Posting Trends")
        try:
            fig4 = plot_trend_line(df)
            if fig4:
                st.pyplot(fig4)
            else:
                st.info("Not enough timestamp data to display trend chart.")
        except Exception as e:
            st.warning(f"Could not render trend chart: {e}")

    # ── Charts Row 3 ──────────────────────────────────────────────────────────
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        st.subheader("🏢 Salary vs Experience")
        try:
            fig5 = plot_experience_salary_box(df)
            if fig5:
                st.pyplot(fig5)
            else:
                st.info("Not enough experience/salary data to display chart.")
        except Exception as e:
            st.warning(f"Could not render experience chart: {e}")

    with row3_col2:
        st.subheader("☁️ Job Title Word Cloud")
        try:
            fig6 = plot_word_cloud(df)
            if fig6:
                st.pyplot(fig6)
            else:
                st.info("Not enough title data to display word cloud.")
        except Exception as e:
            st.warning(f"Could not render word cloud: {e}")

    row4_col1,row4_col2=st.columns(2)

    with row4_col1:
        st.subheader("🔝TOP HIRING COMPANIES🔝")
        try:
            fig7=plot_top_hiring_companies(top_hiring_companies(df))
            if fig7:
                st.pyplot(fig7)
            else:
                st.info("Not enough top hiring companies to display chart.")
        except Exception as e:
            st.warning(f"Could not render top hiring companies: {e}")

        with row4_col2:
            st.subheader("REMOTE VS ONSITE RATIO")
            try:
                fig8=plot_remote_vs_onsite(remote_vs_onsite_ratio(df))
                if fig8:
                    st.pyplot(fig8)
                else:
                    st.info("Not enough Remote vs On Site Ratio data to display chart.")
            except Exception as e:
                st.warning(f"Could not render remote vs onsite ratio: {e}")


    # ── Raw Data Table ────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Raw Job Data")

    # Search inside table
    search = st.text_input("🔎 Search inside table (by title, company, location)", "")
    if search:
        mask = (
            df["title"].astype(str).str.contains(search, case=False, na=False) |
            df["company"].astype(str).str.contains(search, case=False, na=False) |
            df["location"].astype(str).str.contains(search, case=False, na=False)
        )
        st.dataframe(df[mask])
    else:
        st.dataframe(df)

    # ── Download Buttons ──────────────────────────────────────────────────────
    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        csv = df.to_csv(index=False)
        st.download_button(
            "⬇️ Download CSV",
            csv,
            "jobs.csv",
            "text/csv",
            key="download_csv"
        )

    with col_dl2:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='JobsData')
        st.download_button(
            "⬇️ Download Excel",
            data=output.getvalue(),
            file_name="jobs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )

else:
    # ── Welcome screen when no data loaded ───────────────────────────────────
    st.markdown("""
    ## 👋 Welcome to Job Market Analyzer

    Use the sidebar on the left to get started:

    | Option | How |
    |---|---|
    | 🔍 **For Live Scraping** | Enter a job role & location, click "Scrape Jobs Now" |
    | 📂 **Load Saved Data** | Load the pre-collected dataset instantly |
    | ⬆️ **Upload CSV** | Upload your own jobs CSV file |

    ---
    ### 📌 What this tool shows you:
    - 🔥 Top in-demand skills for your target role
    - 💰 Average salaries by city
    - 🌍 Which cities have the most job openings
    - 📈 Job posting trends over time
    - 🏢 Salary range by experience level
    - ☁️ Word cloud of job titles
    """)