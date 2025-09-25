#!/usr/bin/env python3
"""
Quick status check for email automation system
"""

import os
from send_email import load_email_config, read_hr_contacts

print("=== EMAIL AUTOMATION STATUS CHECK ===")
print()

# Check if we're in the right directory
current_files = os.listdir('.')
required_files = ['send_email.py', 'email_config.md', 'hr_contacts.csv']

print("📁 File Check:")
for file in required_files:
    if file in current_files:
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING!")

print()

# Test configuration loading
print("⚙️ Configuration Test:")
config = load_email_config()
if config:
    print(f"   ✅ Config loaded successfully")
    print(f"   📧 Sender: {config.get('sender_name')} <{config.get('sender_email')}>")
    print(f"   ⏱️ Delay: {config.get('email_delay')} seconds")
    print(f"   📄 Resume: {config.get('resume_path')}")
else:
    print("   ❌ Configuration failed to load")

print()

# Test CSV loading  
print("📊 Contact Data Test:")
contacts = read_hr_contacts('hr_contacts.csv')
if contacts:
    print(f"   ✅ {len(contacts)} contacts loaded")
    for i, contact in enumerate(contacts):
        print(f"   {i+1}. {contact.get('name')} at {contact.get('company')}")
else:
    print("   ❌ No contacts loaded")

print()

# Environment check
print("🔑 Environment Check:")
gmail_password = os.getenv('GMAIL_APP_PASSWORD')
if gmail_password:
    print("   ✅ Gmail App Password set in environment")
else:
    print("   ⚠️ Gmail App Password not set (will prompt during send)")

print()
print("=== STATUS SUMMARY ===")
if config and contacts:
    print("🟢 READY TO SEND EMAILS")
    print("💡 Run 'python preview_email.py' to preview")
    print("💡 Run 'python send_email.py' to send emails")
else:
    print("🔴 NOT READY - Fix issues above first")