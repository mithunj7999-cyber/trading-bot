from binance.client import Client
import numpy as np

# Initialize Binance client lazily (will be created on first use)
client = None

def get_client():
    global client
    if client is None:
        client = Client()
    return client

# --- Fibonacci Levels ---
def fibonacci_levels(high, low):
    diff = high - low
    return {
        "23.6%": high - 0.236 * diff,
        "38.2%": high - 0.382 * diff,
        "50%":   high - 0.5 * diff,
        "61.8%": high - 0.618 * diff,
        "78.6%": high - 0.786 * diff,
    }

# --- EMA Calculation ---
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

# --- VWAP Calculation ---
def vwap(candles):
    """
    Calculate Volume Weighted Average Price (VWAP)
    VWAP = Cumulative(Typical Price × Volume) / Cumulative(Volume)
    where Typical Price = (High + Low + Close) / 3
    """
    high = candles['high'].astype(float)
    low = candles['low'].astype(float)
    close = candles['close'].astype(float)
    volume = candles['volume'].astype(float)
    
    # Typical Price
    typical_price = (high + low + close) / 3
    
    # VWAP calculation
    cumulative_tp_vol = (typical_price * volume).cumsum()
    cumulative_vol = volume.cumsum()
    vwap_values = cumulative_tp_vol / cumulative_vol
    
    return vwap_values

# --- Order Book Imbalance ---
def order_book_imbalance(symbol="BTCUSDT", depth=100):
    # Normalize symbol for Binance API (remove slashes, convert to uppercase)
    binance_symbol = symbol.replace('/', '').upper()
    client = get_client()
    order_book = client.get_order_book(symbol=binance_symbol, limit=depth)
    bids = sum([float(bid[1]) for bid in order_book['bids']])
    asks = sum([float(ask[1]) for ask in order_book['asks']])
    imbalance = bids / (bids + asks)
    return imbalance

def generate_signal(candles, symbol="BTCUSDT"):
    closes = candles['close'].astype(float)
    current_price = closes.iloc[-1]

    short_ema = ema(closes, 9).iloc[-1]
    long_ema = ema(closes, 21).iloc[-1]

    highs = candles['high'].astype(float).tail(50).values
    lows = candles['low'].astype(float).tail(50).values
    fib_levels = fibonacci_levels(max(highs), min(lows))

    # Calculate VWAP
    vwap_values = vwap(candles)
    current_vwap = vwap_values.iloc[-1]

    imbalance = order_book_imbalance(symbol)

    # Enhanced signal logic with VWAP and Fibonacci
    if (short_ema > long_ema and 
        imbalance > 0.6 and 
        current_price <= fib_levels["61.8%"] and
        current_price > current_vwap):  # Price above VWAP for uptrend confirmation
        return "BUY", {"imbalance": imbalance, "vwap": current_vwap, "fib_levels": fib_levels}
    elif (short_ema < long_ema and 
          imbalance < 0.4 and 
          current_price >= fib_levels["38.2%"] and
          current_price < current_vwap):  # Price below VWAP for downtrend confirmation
        return "SELL", {"imbalance": imbalance, "vwap": current_vwap, "fib_levels": fib_levels}
    else:
        return "WAIT", {"imbalance": imbalance, "vwap": current_vwap, "fib_levels": fib_levels}
