#!/usr/bin/env python3
"""Pretty print a list of your last ~8 months of Gemini transfers
   plus your current trading portfolio"""
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
BALANCES_URL = "https://api.gemini.com/v1/balances"
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
    headers = ['type', 'timestamp', 'currency', 'amount', 'source']

    # Create a list to hold the data for the table
    table_data = []

    for transfer in my_transfers:
        timestamp = datetime.datetime.fromtimestamp \
                    (transfer['timestampms'] / 1000).strftime('%Y-%m-%d %H:%M')

        if transfer['currency'] == 'BAT':
            USD_VALUE = float(transfer['amount']) * bat_usd_price
        else:
            USD_VALUE = None  # For other currencies, set the USD value to None

        transfer_data = [
            transfer['type'],
            timestamp,
            transfer['currency'],
            f"{float(transfer['amount']):.2f} ({USD_VALUE:.2f} USD)",
            transfer['source']
        ]

        table_data.append(transfer_data)

    print("\nLast ~8 Months of Transactions: \n")
    print(tabulate(table_data, headers=headers))

# Fetch trading balances
payload_balances = {"request": "/v1/balances", "nonce": payload_nonce + 1}
encoded_payload_balances = json.dumps(payload_balances).encode()
b64_balances = base64.b64encode(encoded_payload_balances)
signature_balances = hmac.new(GEMINI_API_SECRET, b64_balances, hashlib.sha384).hexdigest()

request_headers_balances = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'X-GEMINI-APIKEY': GEMINI_API_KEY,
    'X-GEMINI-PAYLOAD': b64_balances,
    'X-GEMINI-SIGNATURE': signature_balances,
    'Cache-Control': "no-cache"
}

balances_response = requests.post(BALANCES_URL, headers=request_headers_balances, timeout=10)
balances_json = balances_response.json()

# Cap BAT amount at 2 decimal places and add USD value in parentheses
for balance in balances_json:
    if balance['currency'] == 'BAT':
        bat_amount = float(balance['amount'])
        bat_usd_value = bat_amount * bat_usd_price
        balance['amount'] = f"{bat_amount:.2f} ({bat_usd_value:.2f} USD)"
    else:
        balance['amount'] = f"{float(balance['amount']):.2f}"

# Print the trading balances using tabulate
print("\nTotal Trading Balances:\n")
print(tabulate([[balance['currency'], \
                 balance['amount']] for balance in balances_json], headers=['currency', 'amount']))
