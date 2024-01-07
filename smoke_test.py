import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def send_slack_notification(webhook_url, message):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Slack notification: {e}")

def check_console_errors(url, webhook_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    # Adding user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        start_time = time.time()  # Start timer for page load

        driver.get(url)
        
        # Wait until the page state becomes "complete" or timeout after 60 seconds
        WebDriverWait(driver, 60).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        load_time = time.time() - start_time  # Calculate page load time

        # Taking screenshots
        driver.save_screenshot("selenium-window-top.png")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Waiting for any lazy-loaded elements
        driver.save_screenshot("selenium-window-bottom.png")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)  # Waiting before taking the final screenshot
        driver.save_screenshot("selenium-window-top-again.png")

        # Collect and print console logs
        console_logs = driver.get_log("browser")
        errors = []
        for log_entry in console_logs:
            print(log_entry)
            if log_entry['level'] == 'SEVERE':
                errors.append(log_entry['message'])

        # Send notification if errors are found
        if errors:
            error_message = f"❌ Errors found in the console logs while loading {url}: {errors}"
            send_slack_notification(webhook_url, error_message)
            sys.exit(1)  # Exit with non-zero status code to indicate failure
        else:
            print("✅ No SEVERE errors found in the console logs while loading the webpage.")
            print(f"⏲️ Page loaded in {load_time:.2f} seconds.")
            load_message = f"Page loaded in {load_time:.2f} seconds."
            send_slack_notification(webhook_url, load_message)

    except Exception as e:
        print(f"Error occurred while loading the webpage: {e}")
        sys.exit(1)  # Exit with non-zero status code to indicate failure
    finally:
        driver.quit()

if __name__ == "__main__":
    url_to_check = os.environ.get("URL")
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if url_to_check is None or webhook_url is None:
        print("Error: Please provide both the URL and the Slack webhook URL as environment variables.")
        sys.exit(1)  # Exit with non-zero status code to indicate failure
    else:
        check_console_errors(url_to_check, webhook_url)
