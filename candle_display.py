import requests
import os

BASE_URL = 'https://testnet.binance.vision/api/v3'

def get_candles_raw(symbol='BTCUSDT', limit=15):
    try:
        r = requests.get(f"{BASE_URL}/klines",
                         params={'symbol': symbol, 'interval': '1m', 'limit': limit})
        return r.json()
    except:
        return []

def draw_candles(data):
    if not data:
        print("   ⚠️  Could not fetch candles")
        return

    candles = []
    for k in data:
        candles.append({
            't': k[0],
            'o': float(k[1]),
            'h': float(k[2]),
            'l': float(k[3]),
            'c': float(k[4]),
            'v': float(k[5])
        })

    # Chart dimensions
    HEIGHT = 12
    WIDTH  = len(candles)

    prices = [c['h'] for c in candles] + [c['l'] for c in candles]
    max_p  = max(prices)
    min_p  = min(prices)
    rng    = max_p - min_p or 1

    def to_row(price):
        return int((max_p - price) / rng * (HEIGHT - 1))

    # Build empty grid
    grid = [[' ' for _ in range(WIDTH * 3)] for _ in range(HEIGHT)]

    for i, c in enumerate(candles):
        bull   = c['c'] >= c['o']
        col    = '\033[92m' if bull else '\033[91m'  # green or red
        reset  = '\033[0m'
        x      = i * 3 + 1

        row_h  = to_row(c['h'])
        row_l  = to_row(c['l'])
        row_o  = to_row(c['o'])
        row_c  = to_row(c['c'])

        top    = min(row_o, row_c)
        bot    = max(row_o, row_c)

        for r in range(HEIGHT):
            if r == row_h:
                grid[r][x] = col + '┬' + reset
            elif r == row_l:
                grid[r][x] = col + '┴' + reset
            elif row_h < r < top:
                grid[r][x] = col + '│' + reset
            elif top <= r <= bot:
                grid[r][x] = col + '█' + reset
            elif bot < r < row_l:
                grid[r][x] = col + '│' + reset

    # Print chart
    print("\n  \033[1m🕯️  LIVE BTC/USDT — 1 MIN CANDLES\033[0m")
    print("  " + "─" * 50)

    for ri, row in enumerate(grid):
        # Price label on right
        price_at = max_p - (rng * ri / (HEIGHT - 1))
        label    = f"  \033[90m{price_at:>10.2f}\033[0m"
        print("  " + ''.join(row) + label)

    print("  " + "─" * 50)

    # Time labels
    times = []
    for i, c in enumerate(candles):
        import datetime
        t = datetime.datetime.fromtimestamp(c['t'] / 1000).strftime('%H:%M')
        if i % 3 == 0:
            times.append(t)
        else:
            times.append('   ')
    print("  " + ' '.join(t[:2] for t in times))
    print()

def print_candle_table(data):
    if not data:
        return

    print("  \033[1m{'Time':<7} {'Open':>9} {'High':>9} {'Low':>9} {'Close':>9}  Dir\033[0m")
    print("  " + "─" * 52)

    for k in data[-6:]:
        import datetime
        t    = datetime.datetime.fromtimestamp(k[0] / 1000).strftime('%H:%M')
        o    = float(k[1])
        h    = float(k[2])
        l    = float(k[3])
        c    = float(k[4])
        bull = c >= o
        col  = '\033[92m' if bull else '\033[91m'
        rst  = '\033[0m'
        arrow = '▲' if bull else '▼'
        print(f"  {col}{t:<7} {o:>9.2f} {h:>9.2f} {l:>9.2f} {c:>9.2f}  {arrow}{rst}")

    print()

def show_candles():
    data = get_candles_raw()
    draw_candles(data)
    print_candle_table(data)