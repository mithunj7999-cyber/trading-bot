import csv, os
from datetime import datetime

buy_price = None

def log_trade(signal, price, sl, tp, imbalance=None, fib_levels=None):
    global buy_price
    file = 'trades.csv'
    write_header = not os.path.exists(file)

    pnl = None
    if signal == 'BUY':
        buy_price = price
    elif signal == 'SELL' and buy_price:
        pnl = round(((price - buy_price) / buy_price) * 100, 2)

    with open(file, 'a', newline='') as f:
        w = csv.writer(f)
        if write_header:
            w.writerow([
                'Date', 'Signal', 'Price', 'StopLoss', 'TakeProfit',
                'PnL%', 'Imbalance', 'FibLevels'
            ])
        w.writerow([
            datetime.now(), signal, price, sl, tp,
            f"{pnl}%" if pnl is not None else "-",
            f"{imbalance:.2f}" if imbalance is not None else "-",
            fib_levels if fib_levels is not None else "-"
        ])

    if pnl is not None:
        emoji = "📈" if pnl > 0 else "📉"
        print(f"{emoji} PnL: {pnl}% | {'PROFIT' if pnl > 0 else 'LOSS'}")
