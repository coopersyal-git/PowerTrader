import requests

# 1. YOUR KEY | flserver.rotman.utoronto.ca
API_KEY = {'X-API-Key': '0QIFNFW3'}

def main():
    with requests.Session() as s:
        s.headers.update(API_KEY)

        # --- STEP 1: CHECK CONNECTION ---
        try:
            case_response = s.get('http://localhost:9999/v1/case')
            
            if case_response.ok:
                tick = case_response.json()['tick']
                print(f"✅ CONNECTION SUCCESSFUL! The case is at tick: {tick}")
            else:
                print(f"❌ Connection failed. Server replied: {case_response.status_code}")
                return # Stop here if we can't connect
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect. Is the RIT Client running?")
            return # Stop here if the bridge is broken

        # --- STEP 2: MAKE THE TRADE ---
        # If we reached this line, the connection is good.
        
        order_params = {
            'ticker': 'TAME',
            'type': 'MARKET',       
            'quantity': 1000,
            'action': 'BUY' 
        }

        print("Attempting to send order...")
        trade_response = s.post('http://localhost:9999/v1/orders', params=order_params)

        if trade_response.ok:
            order_info = trade_response.json()
            print(f"💰 TRADE SUCCESSFUL! Order ID: {order_info['order_id']}")
        else:
            print("⚠️ Trade failed.")
            print(f"Reason: {trade_response.text}")

if __name__ == '__main__':
    main()