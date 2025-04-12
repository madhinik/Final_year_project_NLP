# from flask import Flask, render_template, request, redirect, url_for, session
# import imaplib
# import email
# import smtplib
# from email.message import EmailMessage
# import speech_recognition as sr
# import pyttsx3

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# # Email Credentials
# EMAIL_USER = "dhanapriya988@gmail.com"
# EMAIL_PASS = "said uvzg xujf gflc"

# # Text-to-Speech Engine
# tts = pyttsx3.init()

# import threading

# def talking_tom(text):
#     def speak():
#         tts.say(text)
#         tts.runAndWait()

#     thread = threading.Thread(target=speak)
#     thread.start()

# # Hardcoded Credentials
# VALID_USERNAME = "admin"
# VALID_PASSWORD = "password123"

# # Predefined Email List
# email_list = {
#     "python": "psdhv123@gmail.com",
#     "java": "keerthanan241299@gmail.com",
#     "hello": "gayathrip29603@gmail.com"
# }

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         if username == VALID_USERNAME and password == VALID_PASSWORD:
#             session['logged_in'] = True
#             return redirect(url_for('dashboard'))
#         else:
#             return render_template('login.html', error="Invalid credentials! Please try again.")
#     return render_template('login.html')

# @app.route('/')
# def login_page():
#     return render_template("login.html")

# @app.route('/dashboard')
# def dashboard():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     return render_template('dashboard.html')

# @app.route('/read_email')
# def read_email():
#     try:
#         mail = imaplib.IMAP4_SSL("imap.gmail.com")
#         mail.login(EMAIL_USER, EMAIL_PASS)
#         mail.select("inbox")
        
#         typ, data = mail.search(None, 'ALL')
#         email_ids = data[0].split()
#         if not email_ids:
#             return "No emails found in the inbox."
        
#         first_email_id = email_ids[0]
#         typ, data = mail.fetch(first_email_id, '(RFC822)')
#         raw_email = data[0][1]
#         email_message = email.message_from_bytes(raw_email)

#         subject = email_message["Subject"]
#         sender = email_message["From"]

#         body = ""
#         if email_message.is_multipart():
#             for part in email_message.walk():
#                 if part.get_content_type() == "text/plain":
#                     body = part.get_payload(decode=True).decode()
#                     break
#         else:
#             body = email_message.get_payload(decode=True).decode()

#         mail.logout()
#         return render_template('read_email.html', subject=subject, sender=sender, body=body)
#     except Exception as e:
#         return f"Error: {str(e)}"

# # Send Email with Voice Input
# @app.route('/send_email_voice', methods=['GET', 'POST'])
# def send_email_voice():
#     if request.method == 'POST':
#         recognizer = sr.Recognizer()
#         with sr.Microphone() as source:
#             talking_tom("Speak the recipient's keyword.")
#             recognizer.adjust_for_ambient_noise(source)
#             audio = recognizer.listen(source)

#         try:
#             recipient_key = recognizer.recognize_google(audio).lower()
#             if recipient_key in email_list:
#                 recipient = email_list[recipient_key]
#                 talking_tom(f"Sending email to {recipient_key}")
#                 subject = "Voice Email Test"
#                 body = f"This email is sent to {recipient_key} based on voice input."
#                 send_email(recipient, subject, body)
#                 return f"Email sent to {recipient_key} ({recipient})"
#             else:
#                 return "Recipient not found in the email list."
#         except sr.UnknownValueError:
#             return "Could not understand the audio. Please try again."
#         except sr.RequestError:
#             return "Speech Recognition API error. Please try again later."
    
#     return render_template('send_email_voice.html')

# # Send Email via Text Input
# @app.route('/send_email_text', methods=['GET', 'POST'])
# def send_email_text():
#     if request.method == 'POST':
#         receiver = request.form['receiver']
#         subject = request.form['subject']
#         body = request.form['body']
#         send_email(receiver, subject, body)
#         return redirect(url_for('dashboard'))
#     return render_template('send_email_text.html')

# # Email Sending Function
# def send_email(to_email, subject, body):
#     sender_email = "dhanapriya988@gmail.com"
#     sender_password = "said uvzg xujf gflc"

#     msg = EmailMessage()
#     msg["From"] = sender_email
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.set_content(body)

#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(msg)

#     def recognize_speech():
#         recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         talking_tom("Listening...")
#         recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
#         try:
#             audio = recognizer.listen(source, timeout=5)  # Set a timeout to avoid infinite waits
#             command = recognizer.recognize_google(audio)
#             return command.lower()  # Convert to lowercase for consistency
#         except sr.UnknownValueError:
#             talking_tom("Sorry, I could not understand. Please try again.")
#             return None
#         except sr.RequestError:
#             talking_tom("Speech recognition service is unavailable. Check your internet.")
#             return None

# # Run Flask App
# if __name__ == '__main__':
#     app.run(debug=True)

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

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# Load Email Credentials from Environment Variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

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

@app.route('/read_email')
def read_email():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        typ, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        if not email_ids:
            return "No emails found in the inbox."
        
        first_email_id = email_ids[0]
        typ, data = mail.fetch(first_email_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        subject = email_message["Subject"]
        sender = email_message["From"]

        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()

        mail.logout()
        return render_template('read_email.html', subject=subject, sender=sender, body=body)
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/send_email_voice', methods=['GET', 'POST'])
def send_email_voice():
    if request.method == 'POST':
        recipient_key = request.form['recipient']  # Get from dropdown or input box

        if recipient_key in email_list:
            recipient = email_list[recipient_key]
            subject = "Voice Email Test"
            body = f"This email is sent to {recipient_key} based on button click."
            send_email(recipient, subject, body)

            return f"✅ Email successfully sent to {recipient_key} ({recipient})"
        else:
            return "❌ Recipient not found."

    return render_template('send_email_voice.html', email_list=email_list.keys())



@app.route('/send_email_text', methods=['GET', 'POST'])
def send_email_text():
    if request.method == 'POST':
        receiver = request.form['receiver']
        subject = request.form['subject']
        body = request.form['body']
        send_email(receiver, subject, body)
        return redirect(url_for('dashboard'))
    return render_template('send_email_text.html')

def send_email(to_email, subject, body):
    sender_email = "dhanapriya988@gmail.com"  # Change this
    sender_password = "said uvzg xujf gflc"  # Use an App Password if needed

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            email_message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to_email, email_message)
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
    app.run(debug=True)
