from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example usage of environment variables
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
ASSESSMENT_SPREADSHEET_ID = os.getenv('ASSESSMENT_SPREADSHEET_ID')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_data(range_name):
    """Fetch data from Google Sheets."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=ASSESSMENT_SPREADSHEET_ID, range=range_name).execute()
    return result.get('values', [])

def update_google_sheets_data(range_name, values):
    """Update data in Google Sheets."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    body = {'values': values}
    sheet = service.spreadsheets()
    sheet.values().update(spreadsheetId=ASSESSMENT_SPREADSHEET_ID, range=range_name, valueInputOption='RAW', body=body).execute()


def get_sheet_headings():
    """Scan through the headings in the first row and return all headings with their column IDs."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    range_name = 'Sheet1!1:1'  # First row
    result = sheet.values().get(spreadsheetId=ASSESSMENT_SPREADSHEET_ID, range=range_name).execute()
    headings = result.get('values', [[]])[0]  # Get the first row or an empty list

    # Generate column IDs 
    def get_column_id(index):
        column_id = ""
        while index >= 0:
            column_id = chr(index % 26 + 65) + column_id
            index = index // 26 - 1
        return column_id

    # Map headings to their column IDs
    column_ids = [get_column_id(i) for i in range(len(headings))]
    return {column_ids[i]: headings[i] for i in range(len(headings)) if headings[i]}  # Filter out empty headings