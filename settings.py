import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

iamAccount = 'test-sheets@sheetspython-384910.iam.gserviceaccount.com'
CREDENTIALS_FILE = 'sheetspython-384910-eb3e7afcea17.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
spreadsheetId = '1jx21d4In64A3asHCNVcPVDx5T-ouqC00_v1mT3b2Ik4'