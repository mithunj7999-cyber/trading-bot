# 🤖 Automated Crypto Trading Bot — BTC/USDT

A fully automated cryptocurrency trading bot built in Python that monitors 
the Bitcoin market every 60 seconds and makes intelligent buy and sell 
decisions without any human involvement.

---

## How It Works

The bot runs a continuous cycle every 60 seconds. Each cycle follows the 
same process from start to finish without stopping until you manually shut 
it down.

### Data Collection

Every minute the bot connects to Binance Spot Test Network and downloads 
the last 100 one-minute price candles for the BTC/USDT trading pair. Each 
candle contains the open price, high price, low price, close price, and 
trading volume for that minute. This raw price data is the foundation for 
every decision the bot makes.

### Multi-Layer Signal Analysis

The bot does not trade on a single indicator. It runs five different 
analyses simultaneously and only acts when multiple conditions agree.

**EMA Crossover** — The bot calculates two Exponential Moving Averages. 
EMA 9 tracks the average of the last 9 minutes and reacts quickly to price 
changes. EMA 21 tracks the average of the last 21 minutes and moves slowly. 
When EMA 9 crosses above EMA 21 an uptrend is starting. When EMA 9 crosses 
below EMA 21 a downtrend is starting. This crossover is the primary trigger 
for every trade.

**RSI Filter** — The Relative Strength Index measures market momentum on a 
scale of 0 to 100. A reading above 70 means the market is overbought and a 
BUY would be risky. A reading below 30 means the market is oversold and a 
SELL would be risky. The bot uses RSI as a filter to block signals that 
appear at the worst possible moment.

**VWAP** — Volume Weighted Average Price gives more weight to candles with 
higher trading volume. When the current price is above VWAP the market is 
bullish and buying conditions are favorable. When price is below VWAP the 
market is bearish. The bot only considers BUY signals when price is above 
VWAP.

**Fibonacci Levels** — The bot automatically calculates five Fibonacci 
retracement levels from the recent highest and lowest prices in the last 50 
candles. These levels at 23.6%, 38.2%, 50%, 61.8%, and 78.6% are price 
zones where markets historically tend to reverse. When a signal appears near 
a Fibonacci level it is marked as a stronger confirmation.

**Order Book Imbalance** — The bot reads the live order book from Binance 
and calculates the ratio of buy orders to sell orders waiting to be filled. 
A score above 0.6 means more buyers than sellers are present, indicating 
bullish sentiment. This adds real-time market depth awareness beyond just 
price movement.

### Trade Execution

When the EMA crossover fires and at least VWAP and RSI agree, the bot sends 
a market order to Binance via the REST API. For a BUY signal it purchases 
0.001 BTC instantly at the current market price. For a SELL signal it sells 
the same quantity. Immediately after every BUY the bot calculates a stop 
loss level 2% below the entry price and a take profit level 4% above, 
creating a 1:2 risk to reward ratio on every trade.

### Duplicate Order Prevention

The bot tracks its current position at all times. If it is already holding 
BTC it will ignore any new BUY signal until a SELL has occurred. If it holds 
no position it will ignore any SELL signal. This prevents the bot from 
doubling up accidentally.

### Live Candle Display

Every time the bot runs its cycle it renders a live ASCII candle chart 
directly in the terminal showing the last 15 candles with green blocks for 
bullish candles and red blocks for bearish candles. Price levels are shown 
on the right axis and timestamps on the bottom. Below the chart a table 
shows the last 6 candles with exact open, high, low, and close values.

### Logging and Alerts

Every completed trade is saved to a CSV file with the exact timestamp, 
signal direction, entry price, stop loss, take profit, and profit or loss 
percentage. Simultaneously the bot sends an instant Telegram message to 
the connected phone number with the same trade details so the operator is 
always informed even when away from the computer.

### Performance Dashboard

A separate dashboard module reads the trades CSV at any time and displays 
total trade count, number of wins, number of losses, and cumulative PnL 
percentage so performance can be tracked without opening the log file 
manually.

---

## Architecture
main.py          →  master loop, position tracker, scheduler
data_feed.py     →  fetches live OHLCV candles from Binance API
strategy.py      →  calculates EMA, RSI, VWAP, Fibonacci, order book
executor.py      →  places market buy and sell orders via REST API
logger.py        →  saves trade history to trades.csv with PnL
alerts.py        →  sends Telegram notifications on every trade
candle_display.py →  renders live ASCII candle chart in terminal
dashboard.py     →  displays trade performance summary
config.py        →  central settings for all parameters

---

## Technology Stack

- Python 3.10
- Binance Spot Test Network API
- pandas for data processing
- ta library for technical indicators
- requests for direct HTTP API calls
- python-dotenv for secure credential management
- schedule for automated timing
- Telegram Bot API for real-time alerts

---

## Current Status

This bot is currently running on Binance Testnet using simulated funds. 
All trades, signals, and logs are generated from real market prices but 
no real money is involved. The system is in active testing and performance 
evaluation before any live deployment.

---

## Disclaimer

This project is built for educational and research purposes. Cryptocurrency 
trading carries significant financial risk. Past performance on testnet does 
not guarantee future results on live markets.

---

*Built by Mithun J — BCA Final Year, SSCASC Tumkur University*

