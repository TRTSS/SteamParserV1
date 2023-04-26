import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import settings

httpAuth = settings.credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)

ranges = ['First list!B:B']
res = service.spreadsheets().values().batchGet(
    spreadsheetId=settings.spreadsheetId,
    ranges=ranges,
    valueRenderOption='FORMATTED_VALUE',
    dateTimeRenderOption='FORMATTED_STRING'
).execute()

values = res['valueRanges'][0]['values']
print(values[1:])

prices = []
for link in values[1:]:
    checkFor = ['game_purchase_price', 'game_purchase_price price', 'discount_final_price']
    print(link[0])
    r = requests.get(link[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    price = None
    for c in checkFor:
        price = soup.find('div', class_=c)
        if price is not None:
            break
    if price is None:
        prices.append('Невозможно получить цену')
    else:
        prices.append(price.text.strip())

print(prices)
res = service.spreadsheets().values().batchUpdate(
    spreadsheetId=settings.spreadsheetId,
    body={
        'valueInputOption': 'USER_ENTERED',
        'data': [
            {
                'range': f'First list!C2:C{1 + len(prices)}',
                'majorDimension': 'COLUMNS',
                'values': [
                    prices
                ]
            }
        ]
    }
).execute()