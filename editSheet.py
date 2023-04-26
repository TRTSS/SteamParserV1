import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import settings

httpAuth = settings.credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)

res = service.spreadsheets().values().batchUpdate(
    spreadsheetId=settings.spreadsheetId,
    body={
        'valueInputOption': 'USER_ENTERED',
        'data': [
            {
                'range': 'First list!B2:D5',
                'majorDimension': 'ROWS',
                'values': [
                    ['Test B', 'Test C', 'Test D'],
                    ['24', '5', '=B3/C3']
                ]
            }
        ]
    }
).execute()
