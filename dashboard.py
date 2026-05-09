import pandas as pd
import os

def show_dashboard():
    file = 'trades.csv'
    if not os.path.exists(file):
        print("No trades yet!")
        return

    df = pd.read_csv(file)
    print("\n" + "="*65)
    print("           🤖 TRADING BOT DASHBOARD")
    print("="*65)
    print(df.to_string(index=False))
    print("="*65)

    total_trades = len(df)
    buys  = len(df[df['Signal'] == 'BUY'])
    sells = len(df[df['Signal'] == 'SELL'])

    print(f"\n📊 Total Trades : {total_trades}")
    print(f"✅ BUY Orders  : {buys}")
    print(f"🔴 SELL Orders : {sells}")

    if 'PnL%' in df.columns:
        pnl_rows = df[df['PnL%'] != '-']['PnL%']
        if len(pnl_rows) > 0:
            pnl_values = pnl_rows.str.replace('%','').astype(float)
            wins   = len(pnl_values[pnl_values > 0])
            losses = len(pnl_values[pnl_values < 0])
            print(f"📈 Wins        : {wins}")
            print(f"📉 Losses      : {losses}")
            print(f"💰 Total PnL   : {round(pnl_values.sum(), 2)}%")
    print("="*65 + "\n")

if __name__ == "__main__":
    show_dashboard()