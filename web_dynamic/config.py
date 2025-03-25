import os

class Config:
    DEBUG = True  # Change to False in production
    SECRET_KEY = os.getenv("SECRET_KEY")
