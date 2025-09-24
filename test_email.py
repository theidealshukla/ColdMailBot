#!/usr/bin/env python3
"""
Simple test script to isolate the encoding issue
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def test_simple_email():
    sender_email = "adarshshuklawork@gmail.com"
    recipient_email = "mehuldufarey4@gmail.com"
    
    # Get password
    gmail_password = input("Gmail App Password: ").strip()
    
    # Simple email content with no special characters
    subject = "Test Email - Simple"
    body = "This is a test email with no special characters."
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, gmail_password)
        server.send_message(msg)
        server.quit()
        
        print("Test email sent successfully!")
        return True
        
    except Exception as e:
        print(f"Failed to send test email: {str(e)}")
        return False

if __name__ == "__main__":
    test_simple_email()