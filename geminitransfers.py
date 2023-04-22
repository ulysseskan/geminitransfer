#!/usr/bin/env python3
"""Pretty print a list of your last ~8 months of Gemini transfers
   plus current USD value if currency is BAT"""
import json
import base64
import hmac
import hashlib
import datetime
import time
import requests
from tabulate import tabulate
import config

URL = "https://api.gemini.com/v1/transfers"
GEMINI_API_KEY = config.GEMINI_API_KEY
GEMINI_API_SECRET = config.GEMINI_API_SECRET

t = datetime.datetime.now()
payload_nonce = time.time()
payload = {"request": "/v1/transfers", "nonce": payload_nonce}
encoded_payload = json.dumps(payload).encode()
b64 = base64.b64encode(encoded_payload)
signature = hmac.new(GEMINI_API_SECRET, b64, hashlib.sha384).hexdigest()

request_headers = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'X-GEMINI-APIKEY': GEMINI_API_KEY,
    'X-GEMINI-PAYLOAD': b64,
    'X-GEMINI-SIGNATURE': signature,
    'Cache-Control': "no-cache"
}

response = requests.post(URL, headers=request_headers, timeout=10)

response_json = response.json()

# Get the current price of BAT tokens in USD
ticker_response = requests.get("https://api.gemini.com/v1/pubticker/batusd", timeout=10)
ticker_json = ticker_response.json()
bat_usd_price = float(ticker_json['last'])

if 'result' in response_json and response_json['result'] == 'error':
    print(response_json['message'])
else:
    my_transfers = response_json

    # Specify headers for tabulate
    headers = ['type', 'status', 'timestamp', 'USDvalue', 'currency', 'amount', 'source']

    # Create a list to hold the data for the table
    table_data = []

    BAT_CURRENCY_EXISTS = False

    for transfer in my_transfers:
        timestamp = datetime.datetime.fromtimestamp \
                    (transfer['timestampms'] / 1000).strftime('%Y-%m-%d %H:%M')

        if transfer['currency'] == 'BAT':
            BAT_CURRENCY_EXISTS = True
            USD_VALUE = f"${float(transfer['amount']) * bat_usd_price:.2f}"
        else:
            USD_VALUE = None  # For other currencies, set the USD value to None

        transfer_data = [
            transfer['type'],
            transfer['status'],
            timestamp,
            USD_VALUE,
            transfer['currency'],
            transfer['amount'],
            transfer['source']
        ]

        table_data.append(transfer_data)

    # Print the current BATUSD price if BAT currency exists
    if BAT_CURRENCY_EXISTS:
        print(f"\nCurrent BATUSD price: ${bat_usd_price:.2f}\n")

    # Print the table
    print(tabulate(table_data, headers=headers))
