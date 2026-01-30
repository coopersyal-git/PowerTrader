import requests
import time
import signal
import sys

# CONFIGURATION
API_URL = "http://localhost:9999/v1"
API_KEY = "0QIFNFW3"  # CHECK YOUR TRADER INFO WINDOW FOR THE KEY
TICKER = "CNR"
MAX_POSITION = 25000  # Case limit (check case brief)
ORDER_SIZE = 500      # Size of each clip
SPREAD_THRESHOLD = 0.05 # Minimum profit spread to trade

def get_tick(ticker):
    """Get current market data for the ticker"""
    try:
        resp = requests.get(f"{API_URL}/securities/tick", params={"ticker": ticker})
        return resp.json()
    except Exception as e:
        print(f"Error fetching tick: {e}")
        return None

def get_position(ticker):
    """Get current inventory position"""
    try:
        resp = requests.get(f"{API_URL}/securities", params={"ticker": ticker})
        data = resp.json()
        if data:
            return data[0]['position']
        return 0
    except Exception as e:
        print(f"Error fetching position: {e}")
        return 0

def place_order(ticker, action, quantity, price):
    """Place a Limit order"""
    params = { 
        "ticker": ticker,
        "type": "LIMIT",
        "quantity": quantity,
        "action": action,
        "price": price
    }
    try:
        requests.post(f"{API_URL}/orders", params=params)
        print(f"Placed {action} {quantity} @ {price}")
    except Exception as e:
        print(f"Order failed: {e}")

def main():
    print(f"Starting Market Maker on {TICKER}...")
    
    while True:
        # 1. Get Data
        tick = get_tick(TICKER)
        if not tick:
            continue
# Your existing line
        bid = tick['bid']
        ask = tick['ask']
        spread = ask - bid
        
        # 2. Check current inventory
        position = get_position(TICKER)
        
        # 3. Trading Logic
        # Only trade if spread is profitable
        if spread >= SPREAD_THRESHOLD:
            
            # BUY LOGIC: Only buy if we aren't maxed out on Long position
            if position < MAX_POSITION:
                # Place Buy at current Bid (providing liquidity)
                place_order(TICKER, "BUY", ORDER_SIZE, bid)
            
            # SELL LOGIC: Only sell if we aren't maxed out on Short position
            if position > -MAX_POSITION:
                # Place Sell at current Ask (providing liquidity)
                place_order(TICKER, "SELL", ORDER_SIZE, ask)
                
        else:
            print(f"Spread too tight ({spread:.2f}), waiting...")

        # Sleep to avoid rate limits (adjust based on case speed)
        time.sleep(0.5)

if __name__ == "__main__":
    main()