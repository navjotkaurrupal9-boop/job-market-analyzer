# scraper/base_scraper.py
import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_page(url, retries=3):
    """Fetch a page and return BeautifulSoup object with exponential backoff"""
    for attempt in range(retries):
        try:
            time.sleep(random.uniform(1, 3) * (2 ** attempt))  # Polite delay with exponential backoff
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}. Retrying {attempt + 1}/{retries}...")
    return None

def get_selenium_driver():
    """Setup and return a headless Selenium Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={HEADERS['User-Agent']}")
    
    # Avoid bot detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": HEADERS["User-Agent"]})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver