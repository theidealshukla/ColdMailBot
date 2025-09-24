#!/usr/bin/env python3
"""
Advanced Email Sender Script

This script reads HR contacts from CSV file, generates personalized emails using Gemini API,
and sends them individually via Gmail SMTP.
"""

import smtplib
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

def generate_personalized_email(hr_name, company):
    """
    Generate a personalized email using the custom template.
    
    Args:
        hr_name: Name of the HR contact
        company: Company name
        
    Returns:
        Personalized email content
    """
    try:
        # Clean input data to remove problematic characters
        hr_name = str(hr_name).replace('\xa0', ' ').replace('\u00a0', ' ').strip()
        company = str(company).replace('\xa0', ' ').replace('\u00a0', ' ').strip()
        
        # Custom email template
        email_template = f"""Dear {hr_name},

I am writing to express my interest in the internship opportunity at {company}. As a pre-final year B.Tech Computer Science student at Technocrats Institute of Technology, Bhopal, I have developed a strong foundation in web development and problem-solving, complemented by hands-on experience building real-world projects.

In my academic and project work, I have:

    - Built an AI-powered customer support portal with real-time complaint tracking, Google Authentication, and automated RCA/CAPA suggestions, reducing analysis time by 70%.

    - Developed a responsive news website using JavaScript and Bootstrap, simulating a headless CMS with dynamic content loading.

    - Gained practical experience with JavaScript, React.js, Firebase, Supabase, and Python, alongside deployment tools such as Netlify and Vercel.

I am eager to apply these skills to contribute to {company}, learn from industry professionals, and further sharpen my technical expertise. My strengths in collaboration, adaptability, and problem-solving make me confident in my ability to add value as an intern.

I would welcome the opportunity to discuss how my skills and projects align with your team's needs. Thank you for considering my application.

Sincerely,
Adarsh Kumar Shukla"""
        
        # Clean the final email content and ensure ASCII compatibility
        email_content = email_template.strip()
        # Remove any remaining problematic characters
        email_content = email_content.replace('\xa0', ' ').replace('\u00a0', ' ')
        
        print(f"✅ Generated personalized email for {hr_name} at {company}")
        return email_content
        
    except Exception as e:
        print(f"❌ Error generating email for {hr_name} at {company}: {str(e)}")
        return None

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
    
    # Configuration
    sender_email = "adarshshuklawork@gmail.com"
    csv_file_path = "hr_contacts.csv"
    resume_path = r"c:\Users\Adarsh\OneDrive\Documents\Resume\adarsh resume\Resume.pdf"
    
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
            email_body = generate_personalized_email(hr_name, company)
            if not email_body:
                print(f"   ❌ Failed to generate email content")
                failed_sends += 1
                continue
            
            # Prepare subject
            subject = f"Frontend Internship Application – {company}"
            
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
                print(f"   ⏳ Waiting 3 seconds before next email...")
                time.sleep(3)
                
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