import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

iamAccount = 'test-sheets@sheetspython-384910.iam.gserviceaccount.com'
CREDENTIALS_FILE = 'sheetspython-384910-eb3e7afcea17.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)

spreadsheet = service.spreadsheets().create(body={
    'properties': {
        'title': 'Test',
        'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'First list',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 15
                }
            }
        }
    ]
}).execute()
spreadsheetId = spreadsheet['spreadsheetId']
print(spreadsheetId)
