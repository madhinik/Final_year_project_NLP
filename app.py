from flask import Flask, render_template, request, redirect, url_for, session
import imaplib
import email
import smtplib
from email.message import EmailMessage
import speech_recognition as sr
import pyttsx3
import os
import threading
import difflib
import re
from email.header import decode_header
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# Load Email Credentials from Environment Variables
EMAIL_USER = os.getenv("EMAIL_USER", "dhanapriya988@gmail.com")  # Replace with your email
EMAIL_PASS = os.getenv("EMAIL_PASS", "said uvzg xujf gflc")  # Replace with App Password
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"

# Text-to-Speech Engine
tts = pyttsx3.init()

def talking_tom(text):
    """Speak text using a background thread to avoid blocking the app."""
    def speak():
        tts.say(text)
        tts.runAndWait()
    threading.Thread(target=speak).start()

# Hardcoded Login Credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# Predefined Email List
email_list = {
    "python": "psdhv123@gmail.com",
    "hello": "gayathrip29603@gmail.com"
}

def find_best_match(spoken_word, word_list):
    """Find the best match for recipient name (handles mispronunciations)."""
    matches = difflib.get_close_matches(spoken_word, word_list, n=1, cutoff=0.6)
    return matches[0] if matches else None

def clean_text(text):
    """Remove special characters and keep only readable plain text."""
    # Remove non-printable characters and special symbols (except punctuation)
    return re.sub(r'[^\w\s.,!?@-]', '', text)

@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html', error="Invalid credentials! Please try again.")

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

from email.header import decode_header

def decode_mime_words(s):
    decoded = decode_header(s)
    return ''.join([
        (part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part)
        for part, encoding in decoded
    ])

@app.route('/read_email')
def read_email():
    try:
        # Connect to Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Fetch the latest email
        typ, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        if not email_ids:
            return "No emails found in the inbox."

        latest_email_id = email_ids[-1]  # Get the latest email
        typ, data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        # Decode subject and sender
        subject = decode_mime_words(email_message["Subject"])
        sender = decode_mime_words(email_message["From"])

        # Extract body
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                    elif content_type == "text" and not body:
                        body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = email_message.get_payload(decode=True).decode(errors="ignore")

        mail.logout()

        # Convert to speech
        full_text = f"Email from {sender}. Subject: {subject}. Body: {body}"
        talking_tom(full_text)

        return render_template('read_email.html', subject=subject, sender=sender, body=body)

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/')
def index():
    return render_template('voice_email.html')

@app.route('/send_email_voice', methods=['GET', 'POST'])
def send_email_voice():
    if request.method == 'POST':
        recipient_key = request.form['recipient'].strip().lower()
        subject = request.form['subject']
        body = request.form['email_body']

        email_list = {
            "python": "psdhv123@gmail.com",
            "hello": "gayathrip29603@gmail.com"
        }

        if recipient_key in email_list:
            receiver = email_list[recipient_key]
            send_email(receiver, subject, body)
            return f"<h3>✅ Email successfully sent to {recipient_key} ({receiver})</h3>"
        else:
            return f"<h3>❌ Recipient '{recipient_key}' not found.</h3>"

    # Show the form on GET request
    return render_template('send_email_voice.html')



@app.route('/send_email_text', methods=['GET', 'POST'])
def send_email_text():
    if request.method == 'POST':
        recipient_key = request.form['recipient'].strip().lower()
        subject = request.form['subject']
        body = request.form['body']

        # Predefined email list mapping
        email_list = {
            "python": "psdhv123@gmail.com",
            "hello": "gayathrip29603@gmail.com"
        }

        # Check if the entered name matches a predefined email
        if recipient_key in email_list:
            receiver = email_list[recipient_key]
            send_email(receiver, subject, body)
            return f"✅ Email successfully sent to {recipient_key} ({receiver})"
        else:
            return "❌ Recipient not found."

    return render_template('send_email_text.html')



@app.route('/email_success')
def email_success():
    recipient = request.args.get('recipient', 'unknown')
    talking_tom(f"Email successfully sent to {recipient}")
    return render_template('success.html', recipient=recipient)

def send_email(to_email, subject, body):
    """Sends an email securely using SMTP with TLS and proper MIME formatting."""
    sender_email = EMAIL_USER
    sender_password = EMAIL_PASS

    try:
        # Construct the message with MIMEText
        msg = MIMEText(body, 'plain')  # You can use 'html' for HTML body
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        # Connect and send
        with smtplib.SMTP(SMTP_SERVER, 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

    except Exception as e:
        print("Error:", e)


def recognize_speech(prompt):
    """Recognize voice input and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        talking_tom(prompt)
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            talking_tom("Sorry, I could not understand. Please try again.")
        except sr.RequestError:
            talking_tom("Speech recognition service is unavailable. Check your internet.")
    return None

if __name__ == '__main__':
    app.run(debug=False)
