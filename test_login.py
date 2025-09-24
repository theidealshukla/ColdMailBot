#!/usr/bin/env python3

import smtplib

# Test basic SMTP connection
password = input("Password: ")
print(f"Password length: {len(password)}")
print(f"Password repr: {repr(password)}")

# Check each character
for i, char in enumerate(password):
    if ord(char) > 127:
        print(f"Non-ASCII character at position {i}: '{char}' (ord: {ord(char)})")

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("adarshshuklawork@gmail.com", password)
    print("Login successful!")
    server.quit()
except Exception as e:
    print(f"Login failed: {e}")