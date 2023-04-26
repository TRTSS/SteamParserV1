import json
import socket
import urllib.request
import socks
import httplib2
import urllib3
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import re
import settings
from tenacity import retry, stop_after_attempt, wait_fixed
from handle_http_429_errors import (
    retry_if_http_429_error,
    wait_for_retry_after_header
)

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9050)
socket.socket = socks.socksocket

httpAuth = settings.credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)


def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    return soup.find('body').text


@retry(
    retry=retry_if_http_429_error(),
    wait=wait_for_retry_after_header(fallback=wait_fixed(1)),
    stop=stop_after_attempt(3)
)
def GetItemId(url):
    prices = []
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    # print(url)
    # print(r.data)
    soup = BeautifulSoup(r.data, 'html.parser')

    itemId = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(r.data))
    return itemId


@retry(
    retry=retry_if_http_429_error(),
    wait=wait_for_retry_after_header(fallback=wait_fixed(1)),
    stop=stop_after_attempt(3)
)
def GetData(url, itemId):
    if len(itemId) == 0:
        prices.append(['-', '-', '-'])

    http = urllib3.PoolManager()
    apiURL = f'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid={itemId[0]}&two_factor=0'
    r = http.request('GET', apiURL)
    data = json.loads(r.data)

    if data is None:
        highest_buy = "Не торгуется"
        lower_sell = "Не торгуется"
    else:
        highest_buy = int(data['highest_buy_order']) / 100
        lower_sell = int(data['lowest_sell_order']) / 100

    # prices.append([highest_buy, lower_sell, itemId[0], r.status_code, r.reason])
    return [highest_buy, lower_sell, itemId[0]]


print(f"{checkIP()}")

ranges = ['First list!B:B']
res = service.spreadsheets().values().batchGet(
    spreadsheetId=settings.spreadsheetId,
    ranges=ranges,
    valueRenderOption='FORMATTED_VALUE',
    dateTimeRenderOption='FORMATTED_STRING'
).execute()

values = res['valueRanges'][0]['values']

prices = []
for item in values[1:]:
    print(f"{checkIP()}")
    url = item[0]
    itemId = GetItemId(url)
    data = GetData(url, itemId)
    # soup = BeautifulSoup(r.text, 'html.parser')
    # itemId = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(r.content))
    prices.append(data)

res = service.spreadsheets().values().batchUpdate(
    spreadsheetId=settings.spreadsheetId,
    body={
        'valueInputOption': 'USER_ENTERED',
        'data': [
            {
                'range': f'First list!C2:E{1 + len(prices)}',
                'majorDimension': 'ROWS',
                'values': prices
            }
        ]
    }
).execute()
