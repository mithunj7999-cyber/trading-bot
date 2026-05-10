import os
import schedule, time
from alerts import send_alert
from data_feed import get_candles
from strategy import generate_signal          # ← updated import
from executor import place_order
from logger import log_trade
from config import SYMBOL, TIMEFRAME
from candle_display import show_candles
from datetime import datetime

current_position = None

def run_bot():
    global current_position

    # Clear screen for fresh view
    os.system('clear')

    print(f"\n⏱  {datetime.now().strftime('%H:%M:%S')} — Checking {SYMBOL}...")

    # Show live candles first
    show_candles()

    df = get_candles(SYMBOL, TIMEFRAME)

    # New strategy returns signal and a dictionary with imbalance, vwap, fib_levels
    signal, data = generate_signal(df, symbol=SYMBOL)
    price = df.iloc[-1]['close']
    imbalance = data['imbalance']
    vwap = data['vwap']
    fib_levels = data['fib_levels']

    print(f"   Price   : {price}")
    print(f"   VWAP    : {vwap:.2f}")
    print(f"   Position: {current_position if current_position else 'No position'}")
    print(f"   Imbalance: {imbalance:.2f}")
    print(f"   Fib Levels: {fib_levels}")

    if signal == 'BUY':
        if current_position == 'BUY':
            print("   ⚠️  Already in BUY position — skipping duplicate!")
            return
        order, sl, tp = place_order('BUY')
        if order:
            current_position = 'BUY'
            log_trade('BUY', price, sl, tp, imbalance, fib_levels)
            send_alert(f"🤖 Bot Alert!\nSignal: BUY\nPrice: ${price}\nSL: ${sl}\nTP: ${tp}\nImbalance: {imbalance:.2f}")
            print(f"✅ BUY executed — position opened")

    elif signal == 'SELL':
        if current_position is None:
            print("   ⚠️  No open position to sell — skipping!")
            return
        order, sl, tp = place_order('SELL')
        if order:
            current_position = None
            log_trade('SELL', price, sl, tp, imbalance, fib_levels)
            send_alert(f"🤖 Bot Alert!\nSignal: SELL\nPrice: ${price}\nPosition closed!\nImbalance: {imbalance:.2f}")
            print(f"🔴 SELL executed — position closed")

    else:
        print("   No signal. Waiting...")

schedule.every(1).minutes.do(run_bot)
print("🤖 Bot running on Binance TESTNET — fake money, real prices")
run_bot()
while True:
    schedule.run_pending()
    time.sleep(1)
