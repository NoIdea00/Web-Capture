import os
import re
import sys
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse

# ===== Auto-install dependencies =====
REQUIRED = ["selenium", "playwright", "jinja2", "requests"]
for pkg in REQUIRED:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# Install playwright browsers
subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)

# ===== Imports after installation =====
import requests
from jinja2 import Template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from playwright.sync_api import sync_playwright
from selenium.common.exceptions import WebDriverException

# ===== Configuration =====
INPUT_FILE = "input.txt"
OUTPUT_DIR = "screenshots"
REPORT_FILE = "report.html"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== Utility Functions =====

def sanitize_filename(url):
    return re.sub(r'[^\w\-_.]', '_', url)

def ensure_url_format(url):
    if not url.startswith("http"):
        return "http://" + url
    return url

# ===== Web Capture Functions =====

def capture_with_selenium(url, out_dir):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--headless") ############################################
    chrome_options.add_argument("--start-maximized")

    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.set_page_load_timeout(15)
        driver.get(url)
        time.sleep(3)

        screenshot_path = os.path.join(out_dir, "screenshot.png")
        source_path = os.path.join(out_dir, "page_source.html")

        driver.save_screenshot(screenshot_path)
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        return "Success (Selenium)"
    except Exception as e:
        return f"Failed with Selenium: {e}"
    finally:
        driver.quit()

# fail safe for selenium -------------------------------------------------------------------------------

def capture_with_playwright(url, out_dir):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False) #if want change to true for disable pop up
            page = browser.new_page()
            page.goto(url, timeout=15000)
            time.sleep(3)

            screenshot_path = os.path.join(out_dir, "screenshot.png")
            source_path = os.path.join(out_dir, "page_source.html")

            page.screenshot(path=screenshot_path, full_page=True)
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(page.content())

            browser.close()
            return "Success (Playwright)"
    except Exception as e:
        return f"Failed with Playwright: {e}"
#---------------------------------------------------------------------------------------------------------


def process_url(raw_url):
    url = ensure_url_format(raw_url.strip())
    folder_name = sanitize_filename(raw_url.strip())
    out_dir = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(out_dir, exist_ok=True)

    status = capture_with_selenium(url, out_dir)
    if "Failed" in status:
        status = capture_with_playwright(url, out_dir)

    return {
        "url": url,
        "folder": folder_name,
        "status": status,
        "screenshot": f"{folder_name}/screenshot.png",
        "source": f"{folder_name}/page_source.html"
    }

def generate_report(results):
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Web Capture Report</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .entry { border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; }
            .screenshot { width: 300px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>Web Capture Report</h1>
        {% for r in results %}
        <div class="entry">
            <h2>{{ r.url }}</h2>
            <p>Status: {{ r.status }}</p>
            <a href="screenshots/{{ r.screenshot }}" target="_blank">
                <img src="screenshots/{{ r.screenshot }}" class="screenshot">
            </a><br>
            <a href="screenshots/{{ r.source }}" target="_blank">View Page Source</a>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    template = Template(html_template)
    rendered = template.render(results=results)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(rendered)

# ===== Main Program =====

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    all_results = []
    for url in urls:
        print(f"[+] Processing: {url}")
        result = process_url(url)
        all_results.append(result)

    generate_report(all_results)
    print(f"\n✅ Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()
