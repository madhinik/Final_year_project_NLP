import smtplib
import speech_recognition as sr
from email.message import EmailMessage

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import imaplib
import email
import pyttsx3
import time
from email.message import EmailMessage

username = "dhanapriya988@gmail.com" 
password = "hftb bdcm xowy lcsp"

tts = pyttsx3.Engine()


def talking_tom(text):
    tts.say(text)
    tts.runAndWait()


def login(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    return mail


def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("programing is listening.......")
        audio = recognizer.listen(source)
    try:
        speech = recognizer.recognize_google(audio)
        print("You said: {}".format(speech))
        return speech
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def send_mail(receiver, subject, body):
    sender_email = "dhanapriya988@gmail.com"
    sender_password = "hftb bdcm xowy lcsp"

    # Setup Email Server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create Email Message
    email = EmailMessage()
    email["From"] = sender_email
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(body)

    # Send Email
    server.send_message(email)
    server.quit()

    # Confirm Mail Sent
    print("Your email has been sent successfully!")
    speak_text("Your email has been sent successfully!")

# Main Function
def text_email():
    # Step 1: Ask for Recipient Name
    talking_tom("Please enter the recipient name.")
    recipient_name = input("Enter Recipient Name (e.g., python, hello): ")

    if recipient_name in email_list:
        receiver = email_list[recipient_name]  # Get the actual email address
        talking_tom(f"Email will be sent to {receiver}")
    else:
        talking_tom("Invalid recipient name. Please check the name and try again.")
        return

    # Step 2: Ask for Subject
    talking_tom("Please enter the subject of the email.")
    subject = input("Enter Email Subject: ")
    talking_tom(f"Subject is {subject}")

    # Step 3: Ask for Body
    talking_tom("Please enter the body of the email.")
    body = input("Enter Email Body: ")
    talking_tom(f"Body is {body}")

    # Step 4: Send the Email
    print("Sending the email now.")
    talking_tom("Sending the email now.")
    send_mail(receiver, subject, body)

def mic():
    listenser = sr.Recognizer()
    with sr.Microphone() as source:
        listenser.adjust_for_ambient_noise(source,duration=10)
        print("programing is listening.......")
        audio = listenser.listen(source)
        data = listenser.recognize_google(audio)
        print("You seid",data)
        return data.lower()

##server = smtplib.SMTP("smtp.gmail.com",587)
##server.starttls()
##server.login("techgalwin.tamil26@gmail.com","iyjmxuyrtlvnqysu")
##server.sendmail("techgalwin.tamil26@gmail.com","mariyaaroni09.gsm@gmail.com",data)

email_list = {"python":"psdhv123@gmail.com",
##              "java":"keerthanan241299@gmail.com",
              "hello":"gayathrip29603@gmail.com"}



def send_mail(receiver, subject, body):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("dhanapriya988@gmail.com","hftb bdcm xowy lcsp")
    email = EmailMessage()
    email["From"] ="dhanapriya988@gmail.com"
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(body)
    server.send_message(email)



def main_poc():
    talking_tom("To whom do you want to send this mail?")
    name = mic()
    receiver = email_list[name]
    talking_tom("Speak the subject of the email")
    subject = mic()
    talking_tom("Speak the message of the email")
    body = mic()
    send_mail(receiver, subject, body)
    talking_tom("Your email has been send!!")

def read_latest_email(mail):
    mail.select("inbox")
    typ, data = mail.search(None, 'ALL')
    latest_email_id = data[0].split()[-1]

    typ, data = mail.fetch(latest_email_id, '(RFC822)')
    email_message = email.message_from_bytes(data[0][1])

    subject = email_message['Subject']
    sender = email_message['From']

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                break
    else:
        body = email_message.get_payload(decode=True).decode()

    print("Subject: ", subject)
    print("From: ", sender)
    print("Body: ", body)
    talking_tom(subject)
    talking_tom(sender)
    talking_tom(body)



def main():
    while True:
        talking_tom("Welcome to the Voice-Based Email System.")
        talking_tom("What would you like to do?")
        print("1. Read latest email")
        print("2. Send email")
        print("3. Text email")
        print("4. Exit")
        choice = recognize_speech_from_mic()
        if choice == "read":
            print("Reading latest email...")
            mail = login(username, password)
            read_latest_email(mail)
        elif choice == "send":
            main_poc()
        elif choice == "coding":
            text_email()
        elif choice == "exit":
            talking_tom("Exiting the program.")
            break    
        else:
            print("Invalid choice. Please try again.")
            main()


main()

