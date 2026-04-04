"""
Configuration file for Health Tracker Bot.
Loads environment variables and sets up necessary configurations and application settings for the bot to function properly.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#=====================================
# API KEYS AND CREDENTIALS
#=====================================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

#=====================================
# GOOGLE SHEETS CONFIGURATION
#=====================================
GOOGLE_SHEET_NAME = 'Health Tracker'

#=====================================
# TIMEZONE AND SCHEDULING
#=====================================
TIMEZONE = "America/Toronto"

#Reminder times in 24-hour format (e.g., "08:00", "12:00", "18:00")
WEIGHT_BP_CHECK_TIME = "08:00"
WAIST_CHECK_TIME = "9:00"
WEEKLY_REPORT_TIME = "18:00"
MONTHLY_REPORT_TIME = "20:00"

#=====================================
# HEALTH THERESHOLDS
#=====================================
BP_WARNING_SYSTOLIC_THRESHOLD = 128
BP_WARNING_DIASTOLIC_THRESHOLD = 80

