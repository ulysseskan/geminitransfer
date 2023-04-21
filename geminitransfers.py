#!/usr/bin/env python3
"""Pretty print a list of your last ~8 months of Gemini transfers"""
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

if 'result' in response_json and response_json['result'] == 'error':
    print(response_json['message'])
else:
    my_transfers = response_json

    # Specify headers for tabulate
    headers = ['type', 'status', 'timestamp', 'currency', 'amount', 'destination', 'source']

    # Create a list to hold the data for tabulate
    data = []
    for transfer in my_transfers:
        timestamp = datetime.datetime.fromtimestamp(transfer['timestampms'] / 1000).strftime('%Y-%m-%d %H:%M')
        data.append([
            transfer['type'],
            transfer['status'],
            timestamp,
            transfer['currency'],
            transfer['amount'],
            transfer['destination'],
            transfer['source']
        ])

    # Pretty print the JSON response in columnar spreadsheet style with specific headers
    print(tabulate(data, headers=headers))
