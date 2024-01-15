
import smtplib
import os
from email.message import EmailMessage



def send_email_with_result(result, sender_email, receiver_email):
    try:
        email_password = os.environ.get("EMAIL_PASSWORD") #need to be saved in env variables beforehand
        
        message = EmailMessage()
        message.set_content("Your appointment result: " + result)
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Appointment Alert"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")