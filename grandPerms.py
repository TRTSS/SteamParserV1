import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

iamAccount = 'test-sheets@sheetspython-384910.iam.gserviceaccount.com'
CREDENTIALS_FILE = 'sheetspython-384910-eb3e7afcea17.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

spreadsheetId = '1jx21d4In64A3asHCNVcPVDx5T-ouqC00_v1mT3b2Ik4'
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)

driveService = discovery.build('drive', 'v3', http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId=spreadsheetId,
    body={'type': 'user', 'role': 'writer', 'emailAddress': 'baykalov22882@gmail.com'},
    # Открываем доступ на редактирование
    fields='id'
).execute()
