import ta

def check_signal(df):
    # EMA crossover
    df['ema_short'] = ta.trend.ema_indicator(df['close'], window=9)
    df['ema_long']  = ta.trend.ema_indicator(df['close'], window=21)

    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    ema_buy  = prev['ema_short'] < prev['ema_long'] and last['ema_short'] > last['ema_long']
    ema_sell = prev['ema_short'] > prev['ema_long'] and last['ema_short'] < last['ema_long']

    # RSI filter — only buy when not overbought, only sell when not oversold
    rsi_ok_buy  = last['rsi'] < 70
    rsi_ok_sell = last['rsi'] > 30

    print(f"   RSI: {round(last['rsi'], 1)}")

    if ema_buy and rsi_ok_buy:
        return 'BUY'
    elif ema_sell and rsi_ok_sell:
        return 'SELL'
    return None