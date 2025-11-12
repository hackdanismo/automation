import os
import time
from datetime import datetime

import requests

MONITORED_SITES = [
    {"base": "https://www.frontify.com", "locales": ["en", "fr", "de"]},
    {"base": "https://builtwith.frontify.com", "locales": []},
]

# When to run the script in seconds (1200 seconds = 20 minutes)
CHECK_INTERVAL = 1200

def build_urls(sites) -> list[str]:
    urls: list[str] = []
    for site in sites:
        base = site["base"].rstrip("/")
        locales = site.get("locales") or []

        if locales:
            for locale in locales:
                urls.append(f"{base}/{locale}")
        else:
            urls.append(base)

    return urls

URLS = build_urls(MONITORED_SITES)

def check_site(url: str) -> bool:
    # Returns True if the site is up (status 200-399), otherwise False
    try:
        # Use a HEAD instead of GET request here
        response = requests.head(url, timeout=10, allow_redirects=True)
        return 200 <= response.status_code < 400
    except requests.RequestException:
        return False

def run_checks():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now}] Running uptime check:")

    for url in URLS:
        is_up = check_site(url)
        status_text = "UP" if is_up else "DOWN"
        print(f" {url} -> {status_text}")

if __name__ == "__main__":
    # To run the script locally and not using GitHub Actions:
    # $ LOCAL_LOOP=1 python3 index.py
    if os.getenv("LOCAL_LOOP") == "1":
        while True:
            run_checks()
            time.sleep(CHECK_INTERVAL)
    else:
        # Default for GitHub Actions: run once and exit
        run_checks()