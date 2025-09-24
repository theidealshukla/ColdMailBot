# Email Configuration

This file contains the email template configuration for the ColdMailBot. You can easily edit the subject, body, and attachment settings here without touching the Python code.

## Email Subject Template
```
Internship Application - {company}
```

## Email Body Template
```
Dear {hr_name},

I am writing to express my interest in the internship opportunity at {company}. As a pre-final year B.Tech Computer Science student at Technocrats Institute of Technology, Bhopal, I have developed a strong foundation in web development and problem-solving, complemented by hands-on experience building real-world projects.

In my academic and project work, I have:

- Built an AI-powered customer support portal with real-time complaint tracking, Google Authentication, and automated RCA/CAPA suggestions, reducing analysis time by 70%.

- Developed a responsive news website using JavaScript and Bootstrap, simulating a headless CMS with dynamic content loading.

- Gained practical experience with JavaScript, React.js, Firebase, Supabase, and Python, alongside deployment tools such as Netlify and Vercel.

I am eager to apply these skills to contribute to {company}, learn from industry professionals, and further sharpen my technical expertise. My strengths in collaboration, adaptability, and problem-solving make me confident in my ability to add value as an intern.

I would welcome the opportunity to discuss how my skills and projects align with your team's needs. Thank you for considering my application.

Sincerely,
Adarsh Kumar Shukla
```

## Configuration Settings

### Sender Information
- **Sender Email**: adarshshuklawork@gmail.com
- **Sender Name**: Adarsh Kumar Shukla

### Attachment Settings
- **Resume Path**: c:\Users\Adarsh\OneDrive\Documents\Resume\adarsh resume\Resume.pdf
- **Attachment Name**: Resume.pdf

### Email Delays
- **Delay Between Emails**: 3 seconds

## Template Variables
The following variables will be automatically replaced in the subject and body:
- `{hr_name}` - Name of the HR contact
- `{company}` - Company name
- `{sender_name}` - Your name (from configuration)
- `{sender_email}` - Your email address

## Notes
- Keep the subject line under 50 characters for better deliverability
- Personalize the content while keeping it professional
- Test changes with a small batch before sending to all contacts