
# Bulk Email Sender for Personalized Job Applications

This Python script automates the process of sending personalized internship or job application emails. It reads HR contact information from a CSV file, customizes an email template for each recipient, attaches your resume, and sends it securely using your Gmail account.

## Features

  - **CSV-Powered**: Reads contact details (name, email, company) from a simple `hr_contacts.csv` file.
  - **Dynamic Personalization**: Automatically inserts the HR contact's name and company name into the email subject and body.
  - **Resume Attachment**: Attaches your resume (e.g., a PDF file) to every email.
  - **Secure Authentication**: Uses Gmail's secure App Password system for authentication, so your main password is never exposed in the code.
  - **Rate Limit Friendly**: Includes a built-in delay between sending emails to avoid being flagged as spam by email servers.
  - **Detailed Logging**: Prints real-time status updates to the console for each email being processed.
  - **Final Summary**: Provides a clear summary of successful and failed sends at the end of the campaign.

## Prerequisites

Before you begin, ensure you have the following:

  - Python 3.6 or higher installed on your system.
  - A Google (Gmail) account.
  - Your resume file (e.g., `Resume.pdf`).

## Setup and Installation

Follow these steps to get the script running.

### 1\. Get the Code

Clone this repository or download the `send_email.py` and create the other necessary files.

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

### 2\. Install Dependencies

This script requires the `pandas` library to read the CSV file. Install it using pip:

```bash
pip install pandas
```

### 3\. Configure Your Gmail Account (Critical Step)

To send emails programmatically, you must use a **Gmail App Password**, not your regular account password.

1.  **Enable 2-Factor Authentication (2FA)**: If you haven't already, enable 2FA on your Google Account. You cannot generate an App Password without it.
2.  **Generate an App Password**:
      * Go to your Google Account settings: [https://myaccount.google.com/](https://myaccount.google.com/)
      * Navigate to **Security**.
      * Under "How you sign in to Google," click on **2-Step Verification**.
      * Scroll to the bottom and click on **App passwords**.
      * For "Select app," choose **Mail**.
      * For "Select device," choose **Other (Custom name)** and type something like "Python Email Script".
      * Click **Generate**.
3.  **Save Your Password**: Google will show you a 16-character password. **Copy this password immediately and save it somewhere secure.** You will not be able to see it again. This is the password you will use for the script.

### 4\. Set the App Password

The script reads the App Password from an environment variable for better security.

**For Windows (PowerShell):**

```powershell
$env:GMAIL_APP_PASSWORD='your-16-character-app-password'
```

**For macOS/Linux:**

```bash
export GMAIL_APP_PASSWORD='your-16-character-app-password'
```

> **Note:** The script also allows you to enter the password manually when you run it if the environment variable is not set.

### 5\. Prepare Your Contacts CSV

Create a file named `hr_contacts.csv` in the same directory as the script. It **must** have the following columns: `name`, `email`, and `company`.

**Example `hr_contacts.csv`:**

```csv
name,email,company
Jane Doe,jane.doe@techcorp.com,TechCorp Inc.
John Smith,j.smith@innovate.io,Innovate Solutions
Priya Patel,priya@startupz.dev,Startupz
```

### 6\. Customize the Script

Open the `send_email.py` file and update the following sections:

1.  **Sender and Resume Path:** In the `main()` function, change the `sender_email` and `resume_path` to your own.

    ```python
    def main():
        """Main function to send personalized emails to all HR contacts."""

        # Configuration
        sender_email = "your-email@gmail.com"  # <-- CHANGE THIS
        csv_file_path = "hr_contacts.csv"
        resume_path = r"C:\path\to\your\Resume.pdf" # <-- CHANGE THIS
    ```

2.  **Email Content:** In the `generate_personalized_email()` function, edit the `email_template` with your personal details and cover letter content.

    ```python
    def generate_personalized_email(hr_name, company):
        # ...
        # Custom email template
        email_template = f"""Dear {hr_name},

    I am writing to express my interest in...  <-- EDIT YOUR ENTIRE EMAIL BODY HERE

    Sincerely,
    Your Name"""
        # ...
    ```

## Usage

Once everything is set up, run the script from your terminal:

```bash
python send_email.py
```

The script will start processing the contacts from your CSV file and send emails one by one, printing the progress as it goes.

## Troubleshooting

  - **`smtplib.SMTPAuthenticationError`**: This error almost always means your **App Password** is incorrect or you are using your regular Gmail password. Double-check the 16-character password and ensure 2FA is enabled.
  - **`FileNotFoundError`**: Make sure `hr_contacts.csv` and your resume file are located at the correct paths specified in the script.
  - **Emails go to Spam**: The email content or subject line might be triggering spam filters. Try to make your subject lines unique and the body text as human-like as possible.

-----
