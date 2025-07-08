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