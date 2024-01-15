import requests
import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def process_text(div_text, my_date):
    date_list = []
    for word in div_text.split():
        try:
            date_obj = datetime.strptime(word, "%d.%m.%Y")
            date_list.append(date_obj)
        except ValueError:
            pass  
    date_list.sort()
    current_date = datetime.now()
    my_date_obj = datetime.strptime(my_date, "%d.%m.%Y")
    # Check if the first date in the list is equal to or less than the certain date
    if date_list and date_list[0] <= my_date_obj:
        alert_message = f'An earlier Termin at {date_list[0]} is available. Take action!'
        return alert_message
    return None  



def check_appointment_availability(website_url, my_current_appointment, driver_path):
    response = requests.get(website_url)
    if response.status_code == 200:
        try:
            service = Service(driver_path) # Create a service object pointing to the ChromeDriver
            driver = webdriver.Chrome(service=service) # Create a new instance of the Chrome browser with the service
            driver.get(website_url) # Open the website
            # Close or accept the cookie message or overlay
            cookie_msg_close_button = driver.find_element(By.ID, "cookie_msg_btn_no")
            cookie_msg_close_button.click()
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "button-plus-1027"))
            ).click()
            time.sleep(5) # Wait for the new page to load
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "WeiterButton"))
            ).click()

            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "OKButton"))
            ).click()

            time.sleep(5)  # Wait for the new page to load
            wait = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.onehundred.pull-right"))
            ).click()
            time.sleep(5) 

            div_element = driver.find_element(By.ID, 'sugg_accordion')
            div_text = div_element.text # Extract all text from the <div> element
            # print(div_text)
            result = process_text(div_text, my_date=my_current_appointment)
            if result:
                print(result)
                return result
        finally:
            # Close the browser
            driver.quit()
    else:
        print("Failed to retrieve the website. Status code:", response.status_code)


# # Example usage
if __name__ == "__main__":
    website_url = 'https://www.ingolstadt.de/tevisweb/select2?md=4'
    my_current_appointment='20.03.2024'
    # Path to your ChromeDriver
    driver_path = r"C:\Users\.....\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    result = check_appointment_availability(website_url, my_current_appointment, driver_path)
