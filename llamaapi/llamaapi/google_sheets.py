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

def get_google_sheets_data(table_heading):
    """
    Fetch data from Google Sheets based on the selected table heading.
    The first column stores the 'text' field of the review, and the selected table_heading column contains the categorisation.
    """
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Load all review contents (first column)
    first_column_range = 'Sheet1!A1:A' 
    first_column_result = sheet.values().get(spreadsheetId=ASSESSMENT_SPREADSHEET_ID, range=first_column_range).execute()
    first_column_values = first_column_result.get('values', [])

    # Load all review categorisations based on the selected table heading
    heading_column_range = f'Sheet1!{table_heading}1:{table_heading}'  # Selected column
    heading_column_result = sheet.values().get(spreadsheetId=ASSESSMENT_SPREADSHEET_ID, range=heading_column_range).execute()
    heading_column_values = heading_column_result.get('values', [])

    # Combine the first column and heading column into processed reviews
    processed_reviews = []
    for idx, text_row in enumerate(first_column_values):
        if idx < len(heading_column_values):  # Ensure both columns have data
            processed_reviews.append({
                "id": idx,
                "text": text_row[0],  # First column value
                "rationale": "Example rationale",  # Placeholder rationale
                "categorisation": heading_column_values[idx][0],  # Selected table heading value
                "isCorrect": True,  # Placeholder correctness
            })
    if len(processed_reviews) > 0:
        # Remove the first review (it's just a heading)
        processed_reviews.pop(0)

    return processed_reviews

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
    return {column_ids[i]: headings[i] for i in range(1, len(headings)) if headings[i]}  # filter out empty headings