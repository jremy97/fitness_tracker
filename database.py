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

    def _extract_row_number(self, cell):
        """
        Return a worksheet row number from a gspread Cell-like object.

        In normal gspread usage, worksheet.find() returns a Cell with a
        `.row` attribute. This helper adds a little defensive handling so
        debugging is clearer if a mock or unexpected object is returned.
        """
        if hasattr(cell, "row"):
            return cell.row

        if isinstance(cell, (list, tuple)) and cell:
            first_value = cell[0]
            if isinstance(first_value, int):
                return first_value

        raise TypeError(
            f"Expected worksheet.find() to return a Cell-like object with "
            f"a 'row' attribute, but got {type(cell).__name__}: {cell!r}"
        )

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

        # Find existing user in the user_id column.
        cell = worksheet.find(str(user_id), in_column=1)

        if cell is None:
            # If user does not exist, create a new entry
            worksheet.append_row([user_id, username, email, config.TIMEZONE])
            print(f"Saved new configuration for user Username={username}")
            return

        # If user exists, update their information
        row_num = self._extract_row_number(cell)
        worksheet.update_cell(row_num, 2, username)  # Update username
        worksheet.update_cell(row_num, 3, email)
        print(f"Updated configuration for user Username={username}")

    def get_user_email(self, user_id):
        """
        Retrieves the user's email address from the Google Sheet based on their user ID.
        
        Args:
        - user_id: Unique identifier for the user (e.g., Telegram user ID)
        
        Returns:
        - string: User's email address if found, otherwise None
        """

        worksheet = self.sheet.worksheet("User_Config")

        try:
            cell = worksheet.find(str(user_id), in_column=1)
            if cell is None:
                print(f"No email found for user ID {user_id}")
                return None

            row_num = self._extract_row_number(cell)
            row_values = worksheet.row_values(row_num)
            return row_values[2] # Email is in 3rd column (index 2)
        except Exception as exc:
            print(f"No email found for user ID {user_id}: {exc}")
            return None
    def get_weekly_data(self, user_id):
        """
        Retrieves the user's weight and blood pressure data for the past week from the Google Sheet.
        
        Args:
        - user_id: Unique identifier for the user (e.g., Telegram user ID)
        
        Returns:
        - list of dicts: Each dict contains 'timestamp', 'weight', 'systolic', 'diastolic' for each entry
        """

        worksheet = self.sheet.worksheet("Weight_BP_Log")

        # Get all records from the worksheet as list of dictionaries
        all_records = worksheet.get_all_records()

        # Get the date one week ago from today
        one_week_ago = datetime.now() - timedelta(days=7)

        # Use weekly_data to store the filtered results
        weekly_data = []

        for record in all_records:
            # Is record in the past week and belongs to the user?
            if str(record.get('user_id')) == user_id:
                try:
                    # Parse timestamp string and convert back to datetime object
                    record_time = datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S")
                    if record_time >= one_week_ago:
                        weekly_data.append(record)
                except: 
                    continue

        return weekly_data
    
    def get_monthly_data(self, user_id):
        """
        Retrieves the last 30 days of all health data

        Args:
        - user_id: Unique identifier for the user (e.g., Telegram user ID)

        Returns: 
        - dict: Dictionary with keys "bp_data and "waist_data:
        """
        #Get weight and bp data
        bp_worksheet = self.sheet.worksheet("Weight_BP_Log")
        all_bp_records = bp_worksheet.get_all_records()

        # Get waist measurement data
        waist_worksheet = self.sheet.worksheet("Waist_Log")
        all_waist_records = waist_worksheet.get_all_records()

        # Set time period for last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)

        # Filter BP data for the user and last 30 days
        monthly_bp_data = []
        for record in all_bp_records:
            if str(record.get('user_id')) == user_id:
                try:
                    record_time = datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S")
                    if record_time >= thirty_days_ago:
                        monthly_bp_data.append(record)
                except: 
                        continue
        # Filter waist data for the user and last 30 days
        monthly_waist_data = []
        for record in all_waist_records:
            if str(record.get('user_id')) == user_id:
                try:
                    record_time = datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S")
                    if record_time >= thirty_days_ago:
                        monthly_waist_data.append(record)
                except: 
                        continue
        return {
            "bp_data": monthly_bp_data,
            "waist_data": monthly_waist_data
        }
        


    


















