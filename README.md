
# ColdMailBot - Automated Email Campaign System

This Python script automates the process of sending personalized internship or job application emails. It reads HR contact information from a CSV file, uses customizable email templates from a markdown configuration file, attaches your resume, and sends emails securely using your Gmail account.

## Features

  - **CSV-Powered**: Reads contact details (name, email, company) from a simple `hr_contacts.csv` file.
  - **Markdown Configuration**: Easily customize email subject, body, and settings via `email_config.md` without touching code.
  - **Dynamic Personalization**: Automatically inserts the HR contact's name and company name using template variables.
  - **Resume Attachment**: Attaches your resume (e.g., a PDF file) to every email.
  - **Secure Authentication**: Uses Gmail's secure App Password system for authentication, so your main password is never exposed.
  - **Rate Limit Friendly**: Configurable delay between emails to avoid being flagged as spam.
  - **Detailed Logging**: Prints real-time status updates to the console for each email being processed.
  - **Final Summary**: Provides a clear summary of successful and failed sends at the end of the campaign.
  - **Encoding Safe**: Handles Unicode characters and ensures proper ASCII encoding for reliable email delivery.

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

### 6\. Customize Email Configuration

Open the `email_config.md` file to customize your email content and settings. This file contains:

#### **Email Subject Template**
```
Frontend Internship Application - {company}
```

#### **Email Body Template**
Edit the body section with your personal details and cover letter content:
```
Dear {hr_name},

I am writing to express my interest in the internship opportunity at {company}...

[Add your custom content here]

Sincerely,
Your Name
```

#### **Configuration Settings**
Update the following in the configuration section:
- **Sender Email**: Your Gmail address
- **Sender Name**: Your full name
- **Resume Path**: Full path to your resume file
- **Delay Between Emails**: Time to wait between sends (default: 3 seconds)

#### **Template Variables Available**
- `{hr_name}` - HR contact's name
- `{company}` - Company name
- `{sender_name}` - Your name
- `{sender_email}` - Your email address

**Example customization:**
```markdown
## Configuration Settings

### Sender Information
- **Sender Email**: your-email@gmail.com
- **Sender Name**: Your Full Name

### Attachment Settings
- **Resume Path**: C:\path\to\your\Resume.pdf
```

## Configuration System

### Email Templates (`email_config.md`)

The script uses a markdown configuration file for easy customization without editing Python code:

**Structure:**
- **Email Subject Template**: Customize the subject line
- **Email Body Template**: Write your complete email content
- **Configuration Settings**: Set sender info, resume path, and timing
- **Template Variables**: Use placeholders that get automatically replaced

**Benefits:**
- ✅ No need to edit Python code
- ✅ Easy to modify email content
- ✅ Version control friendly
- ✅ Multiple template support
- ✅ Visual markdown preview

### File Structure
```
internship-automation/
├── send_email.py          # Main script
├── email_config.md        # Email templates and settings
├── hr_contacts.csv        # Contact information
└── README.md             # Documentation
```

## Usage

### Running the Script

Once everything is set up, run the script from your terminal:

```bash
python send_email.py
```

### What Happens:
1. Script loads configuration from `email_config.md`
2. Reads contacts from `hr_contacts.csv`
3. Generates personalized emails using templates
4. Sends emails with your resume attached
5. Provides real-time progress updates
6. Shows final summary of results

### Quick Email Customization

To change your email content:
1. Open `email_config.md` in any text editor
2. Edit the email body template
3. Save the file
4. Run the script - changes apply immediately!

## Advanced Configuration Examples

### Custom Subject Lines
```markdown
## Email Subject Template
```
Passionate Developer Seeking {company} Internship Opportunity
```

### Multi-Paragraph Email Body
```markdown
## Email Body Template
```
Dear {hr_name},

I hope this email finds you well. I am writing to express my strong interest in internship opportunities at {company}.

As a Computer Science student with hands-on experience in web development, I am particularly drawn to {company}'s innovative approach to technology solutions.

Key highlights of my experience:
- Project 1: Description
- Project 2: Description
- Technical skills relevant to your company

I would love to discuss how my skills align with {company}'s goals. Thank you for considering my application.

Best regards,
{sender_name}
{sender_email}
```

### Different Email Delays
```markdown
### Email Delays
- **Delay Between Emails**: 5 seconds  # Slower for better deliverability
```

### Resume Path Examples
```markdown
### Attachment Settings
- **Resume Path**: /Users/yourname/Documents/Resume.pdf           # macOS
- **Resume Path**: C:\Users\YourName\Documents\Resume.pdf        # Windows
- **Resume Path**: /home/yourname/documents/resume.pdf           # Linux
```

## Troubleshooting

### Authentication Issues
- **`smtplib.SMTPAuthenticationError`**: This error almost always means your **App Password** is incorrect or you are using your regular Gmail password. Double-check the 16-character password and ensure 2FA is enabled.
- **Password with spaces**: If you copy-pasted the app password, it might contain invisible characters. The script automatically cleans this, but manually type it if issues persist.

### File Issues
- **`FileNotFoundError`**: Make sure `hr_contacts.csv`, `email_config.md`, and your resume file are located at the correct paths.
- **Configuration not loading**: Ensure `email_config.md` exists in the same directory as `send_email.py`.

### Email Delivery Issues
- **Emails go to Spam**: The email content or subject line might be triggering spam filters. Try to make your subject lines unique and the body text as human-like as possible.
- **Encoding errors**: The script handles Unicode characters automatically, but ensure your `email_config.md` uses standard characters.

### Template Issues
- **Variables not replaced**: Check that you're using the correct variable format: `{variable_name}` in your templates.
- **Template parsing errors**: Ensure the markdown sections in `email_config.md` follow the exact format with proper code blocks.

### Quick Fixes
```bash
# Check if configuration loads correctly
python -c "from send_email import load_email_config; print(load_email_config())"

# Verify Gmail credentials
python -c "import os; print('Password set:', bool(os.getenv('GMAIL_APP_PASSWORD')))"
```

## Why Use Configuration Files?

### Before (Hard-coded in Python)
❌ Need to edit Python code for email changes  
❌ Risk of introducing syntax errors  
❌ Difficult to preview email content  
❌ Not user-friendly for non-programmers  

### After (Markdown Configuration) 
✅ Edit emails in plain text format  
✅ No risk of breaking the script  
✅ Easy to preview in any markdown viewer  
✅ Version control friendly  
✅ Shareable templates across team members  
✅ Instant changes without code modification  

## Contributing

Feel free to submit issues and enhancement requests! This project is designed to be simple yet powerful for job application automation.

## License

This project is open source. Use it responsibly and in accordance with email service provider terms of service.

---

**Happy Job Hunting! 🚀**
