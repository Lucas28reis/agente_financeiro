from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import pandas as pd


class SpreadsheetProcessor:
    @staticmethod
    def process_google_sheet(sheet_id, range_name, credentials_json):
        creds = Credentials.from_service_account_info(credentials_json)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
        values = result.get('values', [])
        
        if not values:
            return {}
        
        headers = values[0]
        data = values[1:]
        
        return {headers[i]: float(row[i]) for row in data for i in range(len(headers))}
    
    @staticmethod
    def process_excel(file_path):
        df = pd.read_excel(file_path)
        return df.to_dict(orient='list')
