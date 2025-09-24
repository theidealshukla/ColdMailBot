#!/usr/bin/env python3
"""
Advanced Email Sender Script

This script reads HR contacts from CSV file, generates personalized emails using Gemini API,
and sends them individually via Gmail SM    print(f"\nStarting email campaign to {len(contacts)} HR contacts")
    print(f"From: {sender_email}")
    print(f"Resume: {resume_path}")
    print("=" * 60)
"""

import smtplib
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import re

def load_email_config(config_file_path="email_config.md"):
    """
    Load email configuration from markdown file.
    
    Args:
        config_file_path: Path to the email configuration markdown file
        
    Returns:
        Dictionary containing email configuration
    """
    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        config = {}
        
        # Extract subject template
        subject_match = re.search(r'## Email Subject Template\s*```\s*\n(.*?)\n```', content, re.DOTALL)
        if subject_match:
            config['subject_template'] = subject_match.group(1).strip()
        else:
            config['subject_template'] = "Internship Application - {company}"
        
        # Extract body template
        body_match = re.search(r'## Email Body Template\s*```\s*\n(.*?)\n```', content, re.DOTALL)
        if body_match:
            config['body_template'] = body_match.group(1).strip()
        else:
            config['body_template'] = "Dear {hr_name},\n\nI am interested in internship opportunities at {company}.\n\nBest regards,\nAdarsh Kumar Shukla"
        
        # Extract sender email
        sender_email_match = re.search(r'- \*\*Sender Email\*\*: (.+)', content)
        if sender_email_match:
            config['sender_email'] = sender_email_match.group(1).strip()
        else:
            config['sender_email'] = "adarshshuklawork@gmail.com"
        
        # Extract sender name
        sender_name_match = re.search(r'- \*\*Sender Name\*\*: (.+)', content)
        if sender_name_match:
            config['sender_name'] = sender_name_match.group(1).strip()
        else:
            config['sender_name'] = "Adarsh Kumar Shukla"
        
        # Extract resume path
        resume_path_match = re.search(r'- \*\*Resume Path\*\*: (.+)', content)
        if resume_path_match:
            config['resume_path'] = resume_path_match.group(1).strip()
        else:
            config['resume_path'] = r"c:\Users\Adarsh\OneDrive\Documents\Resume\adarsh resume\Resume.pdf"
        
        # Extract delay
        delay_match = re.search(r'- \*\*Delay Between Emails\*\*: (\d+)', content)
        if delay_match:
            config['email_delay'] = int(delay_match.group(1))
        else:
            config['email_delay'] = 3
        
        print(f"✅ Successfully loaded email configuration from {config_file_path}")
        return config
        
    except FileNotFoundError:
        print(f"❌ Configuration file {config_file_path} not found. Using default settings.")
        return {
            'subject_template': "Internship Application - {company}",
            'body_template': "Dear {hr_name},\n\nI am interested in internship opportunities at {company}.\n\nBest regards,\nAdarsh Kumar Shukla",
            'sender_email': "adarshshuklawork@gmail.com",
            'sender_name': "Adarsh Kumar Shukla",
            'resume_path': r"c:\Users\Adarsh\OneDrive\Documents\Resume\adarsh resume\Resume.pdf",
            'email_delay': 3
        }
    except Exception as e:
        print(f"❌ Error loading email configuration: {str(e)}")
        return None

def generate_personalized_email(hr_name, company, config):
    """
    Generate a personalized email using the template from configuration.
    
    Args:
        hr_name: Name of the HR contact
        company: Company name
        config: Configuration dictionary loaded from email_config.md
        
    Returns:
        Tuple of (subject, body) for the personalized email
    """
    try:
        # Clean and normalize input data
        hr_name = str(hr_name).strip()
        company = str(company).strip()
        
        # Remove all types of problematic Unicode characters
        unicode_chars_to_remove = ['\xa0', '\u00a0', '\u2009', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u200a', '\u200b', '\u2060', '\ufeff']
        for char in unicode_chars_to_remove:
            hr_name = hr_name.replace(char, ' ')
            company = company.replace(char, ' ')
        
        # Normalize whitespace
        hr_name = ' '.join(hr_name.split())
        company = ' '.join(company.split())
        
        # Convert to ASCII-safe strings
        hr_name = hr_name.encode('ascii', 'ignore').decode('ascii')
        company = company.encode('ascii', 'ignore').decode('ascii')
        
        # Create template variables dictionary
        template_vars = {
            'hr_name': hr_name,
            'company': company,
            'sender_name': config.get('sender_name', 'Adarsh Kumar Shukla'),
            'sender_email': config.get('sender_email', 'adarshshuklawork@gmail.com')
        }
        
        # Generate subject from template
        subject = config.get('subject_template', 'Internship Application - {company}')
        subject = subject.format(**template_vars)
        
        # Generate body from template
        body = config.get('body_template', 'Dear {hr_name},\n\nI am interested in internship opportunities at {company}.\n\nBest regards,\n{sender_name}')
        body = body.format(**template_vars)
        
        # Final cleanup - ensure only ASCII characters
        subject = subject.encode('ascii', 'ignore').decode('ascii')
        body = body.encode('ascii', 'ignore').decode('ascii')
        
        print(f"Generated personalized email for {hr_name} at {company}")
        return subject, body
        
    except Exception as e:
        print(f"Error generating email for {hr_name} at {company}: {str(e)}")
        return None, None

def send_email_via_gmail(sender_email, sender_password, recipient_email, subject, body, attachment_path=None):
    """
    Send email via Gmail SMTP.
    
    Args:
        sender_email: Your Gmail address
        sender_password: Your Gmail app password (not regular password)
        recipient_email: Recipient's email address
        subject: Email subject
        body: Email body text
        attachment_path: Path to attachment file (optional)
    """
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body to email with proper encoding
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            msg.attach(part)
            print(f"✅ Attached resume: {filename}")
        else:
            print("⚠️ Resume file not found - sending without attachment")
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        # Send email using send_message method which handles encoding better
        server.send_message(msg, sender_email, recipient_email)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def read_hr_contacts(csv_file_path):
    """
    Read HR contacts from CSV file.
    
    Args:
        csv_file_path: Path to the CSV file containing HR contacts
        
    Returns:
        List of dictionaries containing HR contact information
    """
    try:
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
        
        df = pd.read_csv(csv_file_path)
        required_columns = ['name', 'email', 'company']
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Remove rows with missing data
        df_clean = df.dropna(subset=required_columns)
        
        if df_clean.empty:
            raise ValueError("No valid HR contacts found in CSV file")
        
        # Clean the data - remove non-breaking spaces and other problematic characters
        for col in required_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str).str.replace('\xa0', ' ').str.strip()
        
        # Convert to list of dictionaries
        contacts = df_clean.to_dict('records')
        print(f"✅ Successfully loaded {len(contacts)} HR contacts")
        
        return contacts
        
    except Exception as e:
        print(f"❌ Error reading HR contacts: {str(e)}")
        return []

def main():
    """Main function to send personalized emails to all HR contacts."""
    
    # Load email configuration from markdown file
    config = load_email_config("email_config.md")
    if not config:
        print("❌ Failed to load email configuration. Exiting.")
        return False
    
    # Configuration from config file
    sender_email = config.get('sender_email', 'adarshshuklawork@gmail.com')
    csv_file_path = "hr_contacts.csv"
    resume_path = config.get('resume_path', r"c:\Users\Adarsh\OneDrive\Documents\Resume\adarsh resume\Resume.pdf")
    email_delay = config.get('email_delay', 3)
    
    # Get Gmail password from environment
    gmail_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not gmail_password:
        print("📧 Gmail App Password Setup Required")
        print("=" * 40)
        print("To send emails via Gmail, you need an 'App Password':")
        print("1. Go to your Google Account settings")
        print("2. Enable 2-Factor Authentication if not already enabled") 
        print("3. Go to Security > 2-Step Verification > App passwords")
        print("4. Generate an app password for 'Mail'")
        print("5. Set it as environment variable: $env:GMAIL_APP_PASSWORD='your-app-password'")
        print("\nOr enter it now (will not be saved):")
        gmail_password = input("Gmail App Password: ").strip()
        
        # Clean the password of any problematic Unicode characters
        unicode_chars_to_remove = ['\xa0', '\u00a0', '\u2009', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u200a', '\u200b', '\u2060', '\ufeff']
        for char in unicode_chars_to_remove:
            gmail_password = gmail_password.replace(char, '')
        
        # Ensure only ASCII characters and remove any remaining spaces
        gmail_password = gmail_password.encode('ascii', 'ignore').decode('ascii')
        gmail_password = ''.join(gmail_password.split())
        
        print(f"Cleaned password length: {len(gmail_password)}")
        
        if not gmail_password:
            print("❌ No password provided. Exiting.")
            return False
    
    # Read HR contacts from CSV
    contacts = read_hr_contacts(csv_file_path)
    if not contacts:
        return False
    
    print(f"\n� Starting email campaign to {len(contacts)} HR contacts")
    print(f"📧 From: {sender_email}")
    print(f"📎 Resume: {resume_path}")
    print("=" * 60)
    
    successful_sends = 0
    failed_sends = 0
    
    # Process each contact
    for i, contact in enumerate(contacts, 1):
        try:
            hr_name = contact['name']
            hr_email = contact['email']
            company = contact['company']
            
            print(f"\n📩 [{i}/{len(contacts)}] Processing {hr_name} at {company}")
            print(f"   Email: {hr_email}")
            
            # Generate personalized email content
            subject, email_body = generate_personalized_email(hr_name, company, config)
            if not email_body or not subject:
                print(f"   ❌ Failed to generate email content")
                failed_sends += 1
                continue
            
            # Send email
            print(f"   📤 Sending email...")
            success = send_email_via_gmail(
                sender_email=sender_email,
                sender_password=gmail_password,
                recipient_email=hr_email,
                subject=subject,
                body=email_body,
                attachment_path=resume_path
            )
            
            if success:
                successful_sends += 1
                print(f"   ✅ Email sent successfully!")
            else:
                failed_sends += 1
                print(f"   ❌ Email sending failed!")
            
            # Add delay between emails to avoid rate limiting
            if i < len(contacts):  # Don't wait after the last email
                print(f"   ⏳ Waiting {email_delay} seconds before next email...")
                time.sleep(email_delay)
                
        except Exception as e:
            print(f"   ❌ Error processing {contact.get('name', 'Unknown')}: {str(e)}")
            failed_sends += 1
            continue
    
    # Final summary
    print("\n" + "=" * 60)
    print(f"📊 EMAIL CAMPAIGN SUMMARY:")
    print(f"   ✅ Successful: {successful_sends}")
    print(f"   ❌ Failed: {failed_sends}")
    print(f"   📧 Total: {len(contacts)}")
    
    if successful_sends > 0:
        print(f"\n🎉 Successfully sent {successful_sends} personalized emails!")
        print("📱 Check your Gmail Sent folder to confirm delivery.")
    
    if failed_sends > 0:
        print(f"\n⚠️  {failed_sends} emails failed to send.")
        print("💡 Check your internet connection and Gmail app password.")
    
    return successful_sends > 0

if __name__ == "__main__":
    main()