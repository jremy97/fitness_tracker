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

        self.sheet = client.open(config.GOOGLE_SHEET_NAME)

        print("Database initialized and connected to Google Sheets.")

    def log_weight_bp(self, user_id, weight, systolic, diastolic):
        """
        Logs the user's weight and blood pressure readings into the Google Sheet.
        
        Args:
        - user_id: Unique identifier for the user (e.g., Telegram user ID)
        - weight: User's weight in kg
        - systolic: Systolic blood pressure reading
        - diastolic: Diastolic blood pressure reading
        """

        # Get the specific worksheet name we want
        worksheet_name = self.sheet.worksheet("Weight_BP_Log")

        # Create a timestamp in readable format
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the new row of data to the worksheet
        worksheet_name.append_row([timestamp, user_id, weight, systolic, diastolic])
        
        # For debugging purposes, print the logged data
        print(f"Logged data for user {user_id} at {timestamp}: Weight={weight}kg, BP={systolic}/{diastolic}mmHg")
    
    def log_waist(self, user_id, waist):
        """
        Logs the user's waist circumference into the Google Sheet.
        
        Args:
        - user_id: Unique identifier for the user (e.g., Telegram user ID)
        - waist: User's waist circumference in Inches
        """

        # Get the specific worksheet name we want
        worksheet_name = self.sheet.worksheet("Waist_Log")

        # Create a timestamp in readable format
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the new row of data to the worksheet
        worksheet_name.append_row([timestamp, user_id, waist])
        
        # For debugging purposes, print the logged data
        print(f"Logged waist circumference for user {user_id} at {timestamp}: Waist={waist}Inches")
    
    def save_user_config(self, user_id, username, email): 

        """
        Saves the user's configuration details (e.g., email) into the Google Sheet.
        If the user already exists, it updates their information instead of creating a new entry.
        If new user, createa new row with the provided details.
        
        Args:
        - user_id: Unique identifier for the user (e.g., Telegram user ID)
        - username: Unique identifier for the user (e.g., Telegram username)
        - email: User's email address for receiving reports
        """

        worksheet = self.sheet.worksheet("User_Config")

        try: 
            # Find existing user
            cell = worksheet.find(str(user_id))

            # If user exists, update their information
            row_num = cell.row
            worksheet.update_cell(row_num, 2, username)  # Update username
            worksheet.update_cell(row_num, 3, email)
            print(f"Updated configuration for user Username={username}")

        except gspread.exceptions.CellNotFound:
            # If user does not exist, create a new entry
            worksheet.append_row([user_id, username, email, config.TIMEZONE])
            print(f"Saved new configuration for user Username={username}")


















