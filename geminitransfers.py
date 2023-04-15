"""Pretty print a list of your last ~8 months of Gemini transfers"""
import json
import base64
import hmac
import hashlib
import datetime
import time
import requests
from tabulate import tabulate

URL = "https://api.gemini.com/v1/transfers"
GEMINI_API_KEY = "yourkey"
GEMINI_API_SECRET = "yoursecret".encode()

t = datetime.datetime.now()
payload_nonce = time.time()
payload =  {"request": "/v1/transfers", "nonce": payload_nonce}
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

my_transfers = response.json()

# Specify headers for tabulate
headers = ['type', 'status', 'currency', 'amount', 'destination', 'source']

# Create a list to hold the data for tabulate
data = []
for transfer in my_transfers:
    data.append([
        transfer['type'],
        transfer['status'],
        transfer['currency'],
        transfer['amount'],
        transfer['destination'],
        transfer['source']
                ])

# Pretty print the JSON response in columnar spreadsheet style with specific headers
print(tabulate(data, headers=headers))
