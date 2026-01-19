import requests

API_KEY = {'X-API-Key': '0QIFNFW3'}

with requests.Session() as s:
    s.headers.update(API_KEY)
    
    # Try with lowercase values
    order_params = {
        'ticker': 'TAME',
        'type': 'LIMIT',
        'quantity': 100,
        'price': 26.00,  # Above current ask to ensure fill
        'action': 'BUY'
    }
    
    print("Trying LIMIT order...")
    trade_response = s.post('http://localhost:9999/v1/orders', params=order_params)
    print(f"Status: {trade_response.status_code}")
    print(f"Response: {trade_response.text}")