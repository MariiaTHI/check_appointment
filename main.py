from appointment import *
from sendemail import send_email_with_result

# # Checking for an earlier appointment
website_url = 'https://www.ingolstadt.de/tevisweb/select2?md=4'
my_current_appointment='20.03.2024'
# Path to your ChromeDriver
driver_path = r"C:\Users\z004urpu\Documents\courses_mylearning\appointment\chromedriver-win64\chromedriver-win64\chromedriver.exe"

if __name__ == "__main__":
    check_interval_seconds = 3600  # Check once every hour 
    while True:
        result = check_appointment_availability(website_url, my_current_appointment, driver_path)
        if result:
            send_email_with_result(result,sender_email='myemail@gmail.com', receiver_email='email@outlook.com')
            break
        time.sleep(check_interval_seconds)