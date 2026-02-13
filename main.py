import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    google_creds, scope
)

client = gspread.authorize(creds)
sheet = client.open_by_key(os.getenv("SPREADSHEET_ID")).sheet1
