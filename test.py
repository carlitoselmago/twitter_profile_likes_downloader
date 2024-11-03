from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Set up the path to geckodriver if needed
#service = Service(executable_path="C:\Users\Administrator\Downloads\geckodriver-v0.35.0-win-aarch64")  # Update if necessary

# Initialize Firefox WebDriver
driver = webdriver.Firefox()

try:
    # Navigate to a page
    driver.get("https://x.com/")

    # Verify the page title
    assert "Example Domain" in driver.title
    print("Page title is correct!")

    # Optionally interact with an element (e.g., a header)
    header = driver.find_element(By.TAG_NAME, "h1")
    print("Header text:", header.text)
    time.sleep(100)

finally:
    # Close the browser
    driver.quit()
