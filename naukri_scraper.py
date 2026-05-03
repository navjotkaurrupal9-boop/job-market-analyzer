# scraper/naukri_scraper.py
import pandas as pd
from datetime import datetime
import os
from .base_scraper import get_selenium_driver
from config import MAX_PAGES, RAW_DATA_PATH
from bs4 import BeautifulSoup
import time
import config

def scrape_naukri():
    jobs = []

    print("Initializing Selenium Driver for Naukri...")
    driver = get_selenium_driver()

    for page in range(0, int(MAX_PAGES)):
        url = (
            f"https://www.naukri.com/"
            f"{config.SEARCH_ROLE.replace(' ', '-')}-jobs-in-"
            f"{config.SEARCH_LOCATION.lower()}?pageNo={page+1}"
        )
        print(f"Scraping Naukri page {page+1}: {url}")

        try:
            driver.get(url)
            time.sleep(6)  # Wait for dynamic content to load fully

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # ── NEW: current Naukri job card wrapper class ──────────────────
            job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

            if not job_cards:
                print(f"No job cards found on page {page+1}. Naukri may have blocked or changed layout.")
                continue

            print(f"Found {len(job_cards)} job cards on page {page+1}")

            for card in job_cards:
                try:
                    # ── Title ────────────────────────────────────────────────
                    # Inside row1 > h2 > a.title
                    title_elem = card.find("a", class_="title")
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                    source_url = title_elem["href"] if title_elem and title_elem.has_attr("href") else url

                    # ── Company ──────────────────────────────────────────────
                    # Inside row2 > span.comp-dtls-wrap > a.comp-name
                    company_elem = card.find("a", class_="comp-name")
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"

                    # ── Experience ───────────────────────────────────────────
                    # Inside row3 > div.job-details > span.exp-wrap
                    exp_elem = card.find("span", class_="exp-wrap")
                    exp = exp_elem.get_text(strip=True) if exp_elem else "Not specified"

                    # ── Location ─────────────────────────────────────────────
                    # Inside row3 > div.job-details > span.loc-wrap
                    loc_elem = card.find("span", class_="loc-wrap")
                    if loc_elem:
                        # Remove the icon span inside loc-wrap if present
                        for icon in loc_elem.find_all("i"):
                            icon.decompose()
                        location = loc_elem.get_text(strip=True)
                    else:
                        location = "Not specified"

                    # ── Salary ───────────────────────────────────────────────
                    # Inside row3 > div.job-details > span.sal-wrap (may not always exist)
                    sal_elem = card.find("span", class_="sal-wrap")
                    if not sal_elem:
                        sal_elem = card.find("span", class_=lambda x: x and "sal" in x.lower())
                    salary = sal_elem.get_text(strip=True) if sal_elem else "Not disclosed"

                    # ── Skills / Description ─────────────────────────────────
                    # Inside row4 > span.job-desc (job description text)
                    # Skills shown as tags below description
                    # Skills from tags list
                    skills = "Not listed"
                    tags_elem = card.find("ul", class_="tags-gt")
                    if tags_elem:
                        tags = [li.get_text(strip=True) for li in tags_elem.find_all("li", class_="tag-li")]
                        if tags:
                            skills = ", ".join(tags)

                    # ── Job Type ─────────────────────────────────────────────
                    location_lower = location.lower()
                    if "remote" in location_lower:
                        job_type = "Remote"
                    elif "hybrid" in location_lower:
                        job_type = "Hybrid"
                    else:
                        job_type = "On-site"

                    from datetime import datetime, timedelta

                    date_elem = card.find("span", class_="job-post-day")
                    posted_text = date_elem.get_text(strip=True).lower() if date_elem else ""

                    # Convert "X days ago" / "X weeks ago" into a real date
                    today = datetime.now()
                    if "today" in posted_text or "hour" in posted_text or "just" in posted_text:
                        posted = today.strftime("%Y-%m-%d")
                    elif "day" in posted_text:
                        days = int(''.join(filter(str.isdigit, posted_text)) or 1)
                        posted = (today - timedelta(days=days)).strftime("%Y-%m-%d")
                    elif "week" in posted_text:
                        weeks = int(''.join(filter(str.isdigit, posted_text)) or 1)
                        posted = (today - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
                    elif "month" in posted_text:
                        months = int(''.join(filter(str.isdigit, posted_text)) or 1)
                        posted = (today - timedelta(days=months * 30)).strftime("%Y-%m-%d")
                    else:
                        posted = today.strftime("%Y-%m-%d")

                    jobs.append({
                        "title"     : title,
                        "company"   : company,
                        "location"  : location,
                        "salary"    : salary,
                        "skills"    : skills,
                        "experience": exp,
                        "job_type"  : job_type,
                        "source"    : "Naukri",
                        "source_url": source_url,
                        "timestamp" : posted,
                        "Posted" :posted
                    })

                except Exception as e:
                    print(f"Error parsing job card: {e}")
                    continue

        except Exception as e:
            print(f"Error loading Naukri page {page+1}: {e}")
            continue

    driver.quit()
    df = pd.DataFrame(jobs)

    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    if not df.empty:
        if os.path.exists(RAW_DATA_PATH):
            df_existing = pd.read_csv(RAW_DATA_PATH)
            df_combined = pd.concat([df_existing, df], ignore_index=True)
            df_combined.to_csv(RAW_DATA_PATH, index=False)
        else:
            df.to_csv(RAW_DATA_PATH, index=False)
        print(f"Scraped {len(df)} jobs successfully from Naukri!")
    else:
        print("No jobs were scraped from Naukri. Site may have blocked the request.")

    return df