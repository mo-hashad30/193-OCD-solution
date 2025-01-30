"""
⚠️ EDUCATIONAL PURPOSES ONLY ⚠️

WARNING: This script is provided for educational purposes only.
Using automated scripts to monitor institutional portals may violate terms of service
and could result in account termination or other consequences.

USE AT YOUR OWN RISK. The developers assume no responsibility for any consequences.
By using this script, you accept all risks and responsibilities.
"""

import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plyer import notification
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import requests
import random

# Load credentials from environment variables (Don't edit, add your credentials in a separate .env file)
load_dotenv()
USERNAME = os.getenv("PORTAL_USERNAME", "")
PASSWORD = os.getenv("PORTAL_PASSWORD", "")
URL = "http://smis.medicine.cu.edu.eg:5555/ords/r/fctstu/kasralainy-edu-eg/login"

# Notification settings
CHECK_INTERVAL = 180  # Time in seconds, PLEASE DO NOT SET THIS BELOW 90, WE DO NOT WANT TO DISTRIBUTE TO MUCH LOAD OR MAKE THIS DETECTED BY THE IT!
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Test mode
TEST_MODE = False  # Set to True for testing, False for normal operation. Use to verify the notification setup.

def play_sound():
    try:
        print('\a')
        os.system('play -nq -t alsa synth 1 sine 440')
    except Exception as e:
        print(f"Error playing sound: {str(e)}")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not set. Skipping Telegram notification.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Telegram notification sent successfully!")
        else:
            print(f"Failed to send Telegram notification: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram notification: {str(e)}")

def send_email(subject, body):
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("Email credentials not set. Skipping email notification.")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def notify_all(title, message, content):
    # Desktop notification
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )
    play_sound()
    # Telegram notification
    send_telegram_message(f"{title}\n\n{content}")
    # Email notification
    send_email(title, f"{message}\n\nContent:\n{content}")

def login(driver):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver.get(URL)
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "P9999_USERNAME"))
            )
            password_field = driver.find_element(By.ID, "P9999_PASSWORD")
            login_button = driver.find_element(By.ID, "B38857912967358407370")

            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            login_button.click()
            print("Logged in successfully.")
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h3[@class='t-Card-title' and text()='Score']/ancestor::a"))
            ).click()
            print("Navigated to Score page.")
            return True

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Login attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                print("Max login attempts reached. Please check your credentials and connection.")
                return False
            time.sleep(5)

def check_for_changes(driver, previous_content):
    try:
        if TEST_MODE:
            # Test mode, not a true check.
            current_time = time.strftime('%H:%M:%S')
            current_content = f"""
            Test Content at {current_time}
            
            Student Name: John Doe
            Student ID: 20193090
            
            Courses:
            1. Medicine 101: {random.choice(['A', 'B+', 'A-'])}
            2. Surgery 202: {random.choice(['A', 'B+', 'A-'])}
            3. Pathology 303: {random.choice(['A', 'B+', 'A-'])}
            """
        else:
            # Normal operation.
            content_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.t-Body-contentInner"))
            )
            current_content = content_element.text.strip()
        
        # Always display the current content on first run.
        print("\nCurrent Content:")
        print("-" * 50)
        print(current_content)
        print("-" * 50)

        if current_content != previous_content:  # Removed previous_content check to test notifications immediately
            print("Change detected! Sending notifications...")
            notify_all(
                "SCORES UPDATED!",
                "Check your portal now!",
                current_content
            )
            
        return current_content

    except TimeoutException:
        print("Score content not found. Re-logging in...")
        return previous_content

def main():
    if TEST_MODE:
        print("Running in TEST MODE - No browser needed")
        previous_content = ""
        try:
            while True:
                previous_content = check_for_changes(None, previous_content)
                print(f"Last checked: {time.strftime('%H:%M:%S')}")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
        return

    # Normal mode with browser
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = '/usr/bin/chromium-browser'

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except WebDriverException as e:
        print(f"Failed to initialize browser driver: {str(e)}")
        return

    previous_content = ""
    
    try:
        while True:
            if not login(driver):
                print("Login failed. Waiting before retry...")
                time.sleep(CHECK_INTERVAL)
                continue
                
            previous_content = check_for_changes(driver, previous_content)
            print(f"Last checked: {time.strftime('%H:%M:%S')}")
            time.sleep(CHECK_INTERVAL)
            driver.refresh()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        if not TEST_MODE:
            driver.quit()

if __name__ == "__main__":
    main()
