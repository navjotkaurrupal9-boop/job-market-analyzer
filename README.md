# 🧑‍💼 Job Market Analyzer

A complete end-to-end data pipeline that scrapes live job listings from Naukri, analyzes the data, and presents insights through an interactive web dashboard — helping job seekers identify in-demand skills, salary trends, and hiring patterns across India.

---

## 📌 What Problem Does This Solve?

Every student and job seeker asks the same questions:
- *Which skills should I learn to get hired?*
- *Which city pays the highest salaries for my role?*
- *Which companies are hiring the most right now?*

Instead of manually browsing hundreds of job listings, this tool automates the entire process and answers all these questions in one interactive dashboard.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔍 Live Scraping | Scrapes real-time job listings from Naukri using Selenium |
| 🧹 Auto Data Cleaning | Removes duplicates, standardizes formats, extracts salary numbers |
| 📊 Skills Analysis | Identifies top in-demand skills across all scraped listings |
| 💰 Salary Analysis | Average salary by city, by experience level |
| 🌍 Location Insights | Job distribution across cities in India |
| 🏢 Company Analysis | Top hiring companies and remote vs on-site ratio |
| 📈 Trend Tracking | Job posting trends over time |
| ☁️ Word Cloud | Visual map of most common job titles |
| 🗄️ Database Storage | All jobs stored in SQLite — no data loss between sessions |
| ⬇️ Export | Download results as CSV or Excel |

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Scraping | Selenium, BeautifulSoup | Browser automation, HTML parsing |
| Data | Pandas | Cleaning, analysis, manipulation |
| Visualization | Matplotlib, Seaborn, WordCloud | Charts and graphs |
| Dashboard | Streamlit | Interactive web interface |
| Database | SQLite | Local job data storage |
| Config | python-dotenv | Secure credential management |

---

## 📁 Project Structure

```
WEB-SCRAPPER-AND-ANALYZER/
│
├── scraper/
│   ├── base_scraper.py        # Selenium driver setup, shared HTTP utilities
│   ├── naukri_scraper.py      # Naukri.com job scraper
│
├── analyzer/
│   ├── cleaner.py             # Data cleaning and preprocessing
│   ├── skills_analyzer.py     # Skill frequency analysis
│   ├── salary_analyzer.py     # Salary, company, job type analysis
│
├── visualizer/
│   ├── charts.py              # All matplotlib/seaborn chart functions
│
├── utils/
│   ├── database.py            # SQLite operations (insert, query, log)
│
├── data/
│   ├── raw/                   # Raw scraped CSV files
│   └── processed/             # Cleaned CSV files
│
├── reports/                   # Auto-generated chart images
│
├── app.py                     # Main Streamlit dashboard
├── main.py                    # Command-line pipeline runner
├── scheduler.py               # Automated 24-hour pipeline scheduler
├── config.py                  # Project settings and constants
├── requirements.txt           # Python dependencies
├── .env                       # Secret credentials (never commit this)
├── .gitignore                 # Files excluded from Git
└── README.md                  # You are here
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/navjotkaurrupal9-boop/job-market-analyzer.git
cd job-market-analyzer
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install ChromeDriver
Selenium requires ChromeDriver matching your Chrome browser version.
Download from: https://chromedriver.chromium.org/downloads
Place it in your system PATH or project root.

### 5. Set up environment variables
Create a `.env` file in the project root:
```
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=receiver_email@gmail.com
```

> ⚠️ **Important:** Use a Gmail App Password, not your regular Gmail password.
> Generate one at: Google Account → Security → 2-Step Verification → App Passwords

### 6. Configure settings
Open `config.py` and set your preferences:
```python
SEARCH_ROLE = "Python Developer"
SEARCH_LOCATION = "Delhi"
MAX_PAGES = 5
HIGH_SALARY_THRESHOLD = 1500000  # 15 LPA
```

---

## ▶️ How to Run

### Option A — Interactive Dashboard (Recommended)
```bash
streamlit run app.py
```
Opens at `http://localhost:8501` in your browser.

**In the dashboard you can:**
- Type a job role and location → click **Scrape Jobs Now** for live data
- Click **Load Saved Data** to use pre-collected dataset
- Upload your own CSV file
- Filter by role and location
- View all 8 charts and download results

### Option B — Command Line Pipeline
```bash
python main.py
```
Runs the full pipeline once and saves charts to `/reports` folder.

### Option C — Automated Daily Scheduler
```bash
python scheduler.py
```
Runs the pipeline immediately, then automatically every 24 hours.
Sends email alerts for high salary jobs found each run.

---

## 📊 Dashboard Preview

### Key Metrics
- Total jobs found
- Number of unique companies hiring
- Cities covered
- Average salary (LPA)

### Charts
1. 🔥 Top In-Demand Skills — horizontal bar chart
2. 💰 Average Salary by Location — bar chart
3. 🌍 Job Distribution by City — pie chart
4. 📈 Job Posting Trends Over Time — line/bar chart
5. 🏢 Salary vs Experience Level — box plot
6. ☁️ Job Titles Word Cloud
7. 🏆 Top Hiring Companies — bar chart
8. 🔄 Remote vs Hybrid vs On-site Ratio — pie chart

---

## ⚠️ Known Limitations

**Naukri bot detection** — Naukri actively detects and blocks automated browsers. The scraper uses random delays and headless Chrome to minimize detection, but occasional blocking is possible. If scraping returns 0 results, try again after a few minutes.

**Indeed blocking** — Indeed India aggressively blocks Selenium-based scrapers. The Indeed scraper is included in the codebase but may not return results consistently without proxy support.

**Selector changes** — Naukri periodically updates their website HTML structure. If the scraper stops finding job cards, the CSS class names in `naukri_scraper.py` may need to be updated by inspecting the live website.

**Salary data** — Not all job listings include salary information. Charts requiring salary data will only reflect listings where salary was disclosed.

---

## 🔮 Future Improvements

- [ ] Add LinkedIn and Glassdoor scrapers
- [ ] Machine learning model to predict salary based on skills and experience
- [ ] Deploy dashboard on Streamlit Cloud for public access
- [ ] Add resume-to-job matching feature
- [ ] Skill gap analyzer — compare your skills vs job requirements
- [ ] WhatsApp alerts using Twilio API
- [ ] Daily automated PDF report generation

---

## 🧰 Requirements

```
streamlit
pandas
plotly
matplotlib
seaborn
requests
beautifulsoup4
selenium
schedule
wordcloud
openpyxl
python-dotenv
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 👩‍💻 Author

**Navjot Kaur**
- 📧 navjotkaurrupal9@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/navjot-kaur-ai-ml-engineer)
- 🐙 [GitHub](https://github.com/navjotkaurrupal9-boop)

---

## 📄 License

This project is for educational purposes. Please respect the Terms of Service of Naukri.com when using the scraping functionality.

---

> *"Built to answer the question every CS student asks — which skills actually get you hired?"*
