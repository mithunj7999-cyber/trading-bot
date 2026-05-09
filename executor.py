import requests, os, time, hmac, hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv
from config import SYMBOL, TRADE_AMOUNT, STOP_LOSS_PCT, TAKE_PROFIT_PCT
load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
BASE_URL = 'https://testnet.binance.vision'

def sign(params):
    query = urlencode(params)
    signature = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    return query + '&signature=' + signature

def place_order(signal):
    symbol_clean = SYMBOL.replace('/', '')
    price_resp = requests.get(f"{BASE_URL}/api/v3/ticker/price", params={'symbol': symbol_clean})
    price = float(price_resp.json()['price'])

    side = 'BUY' if signal == 'BUY' else 'SELL'

    params = {
        'symbol': symbol_clean,
        'side': side,
        'type': 'MARKET',
        'quantity': TRADE_AMOUNT,
        'timestamp': int(time.time() * 1000),
        'recvWindow': 10000
    }

    headers = {'X-MBX-APIKEY': API_KEY}
    url = f"{BASE_URL}/api/v3/order?{sign(params)}"

    try:
        response = requests.post(url, headers=headers)
        order = response.json()

        if signal == 'BUY':
            sl = round(price * (1 - STOP_LOSS_PCT), 2)
            tp = round(price * (1 + TAKE_PROFIT_PCT), 2)
            print(f"✅ BUY  | Price: {price} | SL: {sl} | TP: {tp}")
            return order, sl, tp
        else:
            print(f"🔴 SELL | Price: {price}")
            return order, None, None

    except Exception as e:
        print(f"❌ Order error: {e}")
        return None, None, None