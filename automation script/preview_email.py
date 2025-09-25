#!/usr/bin/env python3
"""
Preview email content without sending
"""

from send_email import load_email_config, generate_personalized_email

# Load configuration
config = load_email_config()
if config:
    print("=== EMAIL CONFIGURATION LOADED ===")
    print(f"Sender: {config['sender_name']} <{config['sender_email']}>")
    print(f"Resume: {config['resume_path']}")
    print(f"Delay: {config['email_delay']} seconds")
    print("\n" + "="*50)
    
    # Test email generation
    subject, body = generate_personalized_email("John Doe", "TechCorp Inc", config)
    
    print("Generated personalized email for John Doe at TechCorp Inc")
    print("=== GENERATED EMAIL PREVIEW ===")
    print(f"Subject: {subject}")
    print(f"\nBody:\n{body}")
else:
    print("❌ Failed to load configuration")