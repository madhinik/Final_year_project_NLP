import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
    EMAIL_USER = "your_email@gmail.com"
    EMAIL_PASSWORD = "your_email_app_password"  # Use App Password, not the actual password
