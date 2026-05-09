import requests, os, pandas as pd
from dotenv import load_dotenv
load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

BASE_URL = 'https://testnet.binance.vision'

def get_candles(symbol, timeframe, limit=100):
    symbol_clean = symbol.replace('/', '')  # BTC/USDT → BTCUSDT
    url = f"{BASE_URL}/api/v3/klines"
    params = {
        'symbol': symbol_clean,
        'interval': timeframe,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp','open','high','low','close','volume',
        'close_time','quote_volume','trades',
        'taker_buy_base','taker_buy_quote','ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df