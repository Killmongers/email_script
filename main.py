from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def send_email(to_email: str, subject: str, resume_file: UploadFile) -> bool:
    body = """
Dear Hiring Manager,

I hope this message finds you well.

I am writing to express my interest in any available on-site roles as a Python Developer or DevOps Engineer. I recently completed a 6-month internship where I worked on backend development, automation, and cloud deployment. I also built a WhatsApp chatbot using Python and integrated it with real-time APIs.

I am eager to bring my skills and enthusiasm to your team and grow in a challenging environment.

Please find my resume attached for your reference. I would be grateful for the opportunity to discuss how I can contribute.

Thank you for your time and consideration.

Best regards,  
Swastik Moolya  
📞 +91-9327973365  
✉️ moolyaswastik48@gmail.com  
🔗 [GitHub](https://github.com/Killmongers) | [LinkedIn](https://www.linkedin.com/in/swastik-python-dev)
"""

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        resume_content = resume_file.file.read()
        part = MIMEApplication(resume_content, Name=resume_file.filename)
        part['Content-Disposition'] = f'attachment; filename="{resume_file.filename}"'
        msg.attach(part)
    except Exception as e:
        print(f"❌ Failed to attach file: {e}")
        return False

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

@app.post("/send-email")
async def handle_email(
    to_email: str = Form(...),
    subject: str = Form(...),
    resume: UploadFile = File(...)
):
    success = send_email(to_email, subject, resume)
    return {"message": "✅ Email sent!"} if success else {"error": "❌ Email failed!"}

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))  # Render sets the PORT environment variable
    uvicorn.run("main:app", host="0.0.0.0", port=port)
