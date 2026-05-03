from dotenv import load_dotenv
import os
load_dotenv()

# Scraping settings
SEARCH_ROLE = ""
SEARCH_LOCATION = ""
MAX_PAGES = 5

# Database
DB_PATH = os.getenv('DB_PATH')

# File paths
RAW_DATA_PATH = os.getenv('RAW_DATA_PATH')
CLEAN_DATA_PATH = os.getenv('CLEAN_DATA_PATH')

# Email alert settings
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

# Top skills to track
SKILLS_LIST = [
    "python", "django", "flask", "sql", "machine learning",
    "pandas", "numpy", "aws", "docker", "git", "fastapi",
    "tensorflow", "pytorch", "mongodb", "postgresql"
]

# Driver waits
PAGE_LOAD_WAIT = 10
ELEMENT_WAIT = 5

# Alert thresholds
HIGH_SALARY_THRESHOLD = 1500000  # e.g., 15 LPA

# Indeed settings
INDEED_URL = os.getenv('INDEED_URL')