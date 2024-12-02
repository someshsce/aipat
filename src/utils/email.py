import os
import re
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, EmailStr, ValidationError

env_path = os.path.join(os.path.expanduser("~"), ".aipatt.env")
load_dotenv(env_path)

SMTP_SERVER=os.getenv("SMTP_SERVER", "smtp.gmail.com")
PORT=os.getenv("PORT", "465")
USERNAME=os.getenv("USERNAME")
PASSWORD=os.getenv("PASSWORD")

class EmailInput(BaseModel):
    recipient: EmailStr
    subject: str
    body: str

def render_template(subject: str, body: str):
    """
    Generates an HTML email body with styling and a footer.
    """
    formated_body = body.replace("\n", "<br>")
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            .email-header {{
                font-size: 12px;
                font-weight: bold;
                color: #0056b3;
                margin-bottom: 20px;
                text-align: center;
            }}
            .email-body {{
                font-size: 14px;
                color: #333;
                margin-bottom: 20px;
            }}
            .email-footer {{
                font-size: 7px;
                color: #888;
                text-align: center;
                margin-top: 20px;
                border-top: 1px solid #ddd;
                padding-top: 9px;
            }}
            .email-footer a {{
                color: #0056b3;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">{subject}</div>
            <div class="email-body">
                <p>{formated_body}</p>
                <br>
                <p>Best regards, <strong>AIPATT</strong></p>
            </div>
            <div class="email-footer">
                This email was sent by <strong>AIPATT: An AI Powered Assistance Tool for Terminals</strong><br>
            </div>
        </div>
    </body>
    </html>
    """

def send_html_email(subject: str, body: str, recipient_list: list):
    """
    Sends an HTML email with a plain text fallback.
    """
    try:
        if not recipient_list:
            return "Recipient list is empty. Please provide at least one recipient."

        html_content = render_template(subject, body)
        plain_text = f"{subject}\n\n{body}\n\nBest regards,\nAIPATT"

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"AIPATT <{USERNAME}>"
        msg["To"] = ", ".join(recipient_list)

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP_SSL(SMTP_SERVER, PORT) as smtp:
            smtp.login(USERNAME, PASSWORD)
            smtp.sendmail(USERNAME, recipient_list, msg.as_string())

        return "Email sent successfully."
    except smtplib.SMTPAuthenticationError:
        return "Authentication failed. Please check your email username and password."
    except smtplib.SMTPConnectError as e:
        return f"Failed to connect to the server: {e}"
    except smtplib.SMTPException as e:
        return f"SMTP error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def clean_email_body(subject: str, body: str) -> str:
    """
    Cleans the email body by:
    - Removing duplicate or misplaced subjects.
    - Trimming unnecessary trailing notes or lines.
    - Ensuring proper structure for the email content.
    """
    subject = subject.strip()
    subject_pattern = re.escape(subject)
    body = re.sub(rf"(?i)^subject:\s*{subject_pattern}\s*", "", body, flags=re.MULTILINE)
    body = re.sub(rf"(?i)subject:\s*{subject_pattern}\s*", "", body, flags=re.MULTILINE)

    body = re.sub(r"(?i)^subject:\s*.*$", "", body, flags=re.MULTILINE)

    trailing_notes_pattern = r"(Note:.*|Disclaimer:.*|Generated content:.*)$"
    body = re.sub(trailing_notes_pattern, "", body, flags=re.IGNORECASE).strip()

    signature_patterns = r"(Best regards,.*|Regards,.*|Sincerely,.*|Thanks,.*|Cheers,.*|Yours truly,.*|Yours faithfully,.*|Yours sincerely,.*|Yours,.*|Warm regards,.*|Warmly,.*|Warmest regards,.*|With best regards,.*|With kind regards,.*|With regards,.*|With warm,.*|With warmest)"
    body = re.split(signature_patterns, body, flags=re.IGNORECASE)[0].strip()

    return body

def compose_and_send_email(data: EmailInput):
    """
    Accepts an EmailInput object and sends the email after displaying the draft.
    """
    recipient = data.recipient
    subject = data.subject or "No Subject Provided"
    body = clean_email_body(subject, data.body)

    email_draft = f"""
--- Draft Email ---
To: {recipient}
Subject: {subject}

{body}

Best regards, AIPATT
-------------------
    """
    print(email_draft)

    confirmation = input("Do you want to send this email? (y/n): ").strip().lower()
    if confirmation in ['y', 'yes']:
        return send_html_email(subject, body, [recipient])
    else:
        return "Email not sent."

email_tool = StructuredTool(
    name="Send Email",
    func=compose_and_send_email,
    description="Compose and send an email. Input should include 'recipient', 'subject', and 'body'.",
    args_schema=EmailInput
)
