# database.py
"""
Database layer for Health Tracker Bot.
Handles all interactions with the Google Sheets database, including reading and writing user data, health metrics,
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import config

class HealthDatabase:
    """
    Manages all data storage operations using Google Sheets.
    
    This class abstracts away the complexity of Google Sheets API,
    providing simple methods like log_weight_bp() instead of
    forcing the rest of the code to understand spreadsheet operations.
    """

    # Defines Google APIs we need to access
    def __init__(self):

        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
    
        # Load credentials from the JSON file
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

        # Authorize and create client
        client = gspread.authorize(creds)

        self.sheet = self.client.open(config.GOOGLE_SHEET_NAME)

        print("Database initialized and connected to Google Sheets.")






