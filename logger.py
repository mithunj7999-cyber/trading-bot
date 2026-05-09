import csv, os
from datetime import datetime

buy_price = None

def log_trade(signal, price, sl, tp):
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
            w.writerow(['Date','Signal','Price','StopLoss','TakeProfit','PnL%'])
        w.writerow([datetime.now(), signal, price, sl, tp,
                    f"{pnl}%" if pnl is not None else "-"])

    if pnl is not None:
        emoji = "📈" if pnl > 0 else "📉"
        print(f"{emoji} PnL: {pnl}% | {'PROFIT' if pnl > 0 else 'LOSS'}")