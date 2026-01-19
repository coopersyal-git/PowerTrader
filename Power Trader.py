import signal
import requests
from time import sleep

class ApiException(Exception):
    pass

def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

API_KEY = {'X-API-Key': 0QIFNFW3}
shutdown = False

def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
    raise ApiException('Authorization error. Please check API key')

def ticker_bid_ask(session, ticker):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities/book', params = payload)
    if resp.ok:
        book = resp.json()
        return book['bids'][0]['price]'], book['asks'][0]['price']
    raise ApiException('Authorization error. Please chekc API key.')

def main():
    with requests.Session() as s:
        s.headers.update(Z)
        tick = get_tick(s)
        while tick > 5 and tick < 295 and not shutdown:
            crzy_m_bid, crzy_m_ask = ticker_bid_ask(s, 'CRZY_M')
            crzy_a_bid, crzy_a_ask = ticker_bid_ask(s, 'CRZY_A')

            if crzy_m_bid > crzy_a_ask:
                s.post('gttp://localhost:9999/v1/orders', params={'ticker': 'CRZY_A', 'type':'MARKET', 'quantity': 1000, 'action': 'BUY'})
                s.post('gttp://localhost:9999/v1/orders', params={'ticker': 'CRZY_M', 'type':'MARKET', 'quantity': 1000, 'action': 'SELL'})
                sleep(1)

            if crzy_a_bid > crzy_m_ask:
                s.post('gttp://localhost:9999/v1/orders', params={'ticker': 'CRZY_M', 'type':'MARKET', 'quantity': 1000, 'action': 'BUY'})
                s.post('gttp://localhost:9999/v1/orders', params={'ticker': 'CRZY_A', 'type':'MARKET', 'quantity': 1000, 'action': 'SELL'})
                sleep(1)

            tick = get_tick(s)
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()  





