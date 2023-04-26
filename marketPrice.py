import json

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import re
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
for item in values[1:]:
    print(item[0])
    url = item[0]

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    itemId = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(r.content))
    print(itemId)

    apiURL = f'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid={itemId[0]}&two_factor=0'
    r = requests.get(apiURL)
    data = json.loads(r.text)
    print(data)

    if data is None:
        highest_buy = "Не торгуется"
        lower_sell = "Не торгуется"
    else:
        highest_buy = int(data['highest_buy_order']) / 100
        lower_sell = int(data['lowest_sell_order']) / 100

    prices.append([highest_buy, lower_sell, itemId[0], r.status_code])

res = service.spreadsheets().values().batchUpdate(
    spreadsheetId=settings.spreadsheetId,
    body={
        'valueInputOption': 'USER_ENTERED',
        'data': [
            {
                'range': f'First list!C2:F{1 + len(prices)}',
                'majorDimension': 'ROWS',
                'values': prices
            }
        ]
    }
).execute()
