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

def load_email_config(primary_md="email_config.md", fallback_txt="email_config.txt"):
    """Load email configuration preferring markdown, with TXT fallback.

    Markdown format expectations:
      ## Email Subject Template  (code block with subject)
      ## Email Body Template     (code block with body)
      Configuration Settings list style lines for sender, resume, delay.

    Fallback TXT format supports:
      - KEY=VALUE or KEY: VALUE
      - [BODY] ... [/BODY]
    """

    def _apply_defaults(cfg: dict):
        cfg.setdefault('subject_template', "Internship Application - {company}")
        cfg.setdefault('body_template', "Dear {hr_name},\n\nI am interested in internship opportunities at {company}.\n\nBest regards,\nAdarsh Kumar Shukla")
        cfg.setdefault('sender_email', "adarshshuklawork@gmail.com")
        cfg.setdefault('sender_name', "Adarsh Kumar Shukla")
        cfg.setdefault('resume_path', r"c:\Users\Adarsh\OneDrive\Documents\Resume\adarsh resume\Resume.pdf")
        cfg.setdefault('email_delay', 3)
        return cfg

    # First try markdown
    if os.path.exists(primary_md):
        try:
            with open(primary_md, 'r', encoding='utf-8') as f:
                content = f.read()
            cfg: dict[str, str | int] = {}
            # Subject code block
            subj_match = re.search(r'##\s*Email Subject Template.*?```(.*?)```', content, re.DOTALL | re.IGNORECASE)
            if subj_match:
                cfg['subject_template'] = subj_match.group(1).strip().splitlines()[0].strip()
            # Body code block
            body_match = re.search(r'##\s*Email Body Template.*?```(.*?)```', content, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_block = body_match.group(1).strip()
                cfg['body_template'] = body_block
            # Sender email
            sender_email = re.search(r'Sender Email\*?\*?\s*:\s*([^\n]+)', content, re.IGNORECASE)
            if sender_email:
                cfg['sender_email'] = sender_email.group(1).strip()
            sender_name = re.search(r'Sender Name\*?\*?\s*:\s*([^\n]+)', content, re.IGNORECASE)
            if sender_name:
                cfg['sender_name'] = sender_name.group(1).strip()
            resume_path = re.search(r'Resume Path\*?\*?\s*:\s*([^\n]+)', content, re.IGNORECASE)
            if resume_path:
                cfg['resume_path'] = resume_path.group(1).strip()
            delay = re.search(r'Delay Between Emails\*?\*?\s*:\s*(\d+)', content, re.IGNORECASE)
            if delay:
                cfg['email_delay'] = int(delay.group(1))

            _apply_defaults(cfg)
            print(f"✅ Loaded markdown configuration from {primary_md}")
            return cfg
        except Exception as e:
            print(f"⚠️ Failed to parse markdown config ({e}). Trying TXT fallback...")

    # Fallback to TXT
    if os.path.exists(fallback_txt):
        try:
            with open(fallback_txt, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            cfg: dict[str, str | int] = {}
            in_body = False
            body_lines: list[str] = []
            for raw in lines:
                line = raw.rstrip('\n')
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                if stripped.upper() == '[BODY]':
                    in_body = True
                    body_lines = []
                    continue
                if stripped.upper() == '[/BODY]':
                    in_body = False
                    cfg['body_template'] = '\n'.join(body_lines).strip()
                    continue
                if in_body:
                    body_lines.append(line)
                    continue
                if '=' in stripped:
                    k, v = stripped.split('=', 1)
                elif ':' in stripped:
                    k, v = stripped.split(':', 1)
                else:
                    continue
                k = k.strip().upper(); v = v.strip()
                if k == 'SUBJECT': cfg['subject_template'] = v
                elif k == 'SENDER_EMAIL': cfg['sender_email'] = v
                elif k == 'SENDER_NAME': cfg['sender_name'] = v
                elif k == 'RESUME_PATH': cfg['resume_path'] = v
                elif k == 'EMAIL_DELAY':
                    try: cfg['email_delay'] = int(v)
                    except ValueError: print('⚠️ EMAIL_DELAY invalid, using default.')
            _apply_defaults(cfg)
            print(f"✅ Loaded text configuration from {fallback_txt}")
            return cfg
        except Exception as e:
            print(f"❌ Error parsing text config: {e}")

    print("❌ No configuration file found. Using defaults.")
    return _apply_defaults({})

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
    
    # Load email configuration (markdown preferred, txt fallback)
    config = load_email_config()
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