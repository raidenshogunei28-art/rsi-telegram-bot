import yfinance as yf
from ta.momentum import RSIIndicator
import requests
import time

TOKEN = "ISI_TOKEN_BOT"
CHAT_ID = "ISI_CHAT_ID"

pairs = [

# FOREX
"EURUSD=X",
"GBPUSD=X",
"USDJPY=X",
"AUDUSD=X",
"USDCAD=X",
"USDCHF=X",
"NZDUSD=X",

# GOLD SILVER
"GC=F",
"SI=F",

# CRYPTO
"BTC-USD",
"ETH-USD",
"SOL-USD",
"XRP-USD",
"DOGE-USD",
"BNB-USD",
"ADA-USD",
"MATIC-USD",
"LTC-USD",
"TRX-USD"
]

last_signal = {}

def send_telegram(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def check_rsi():

    print("Scanning market...")

    for pair in pairs:

        try:

            data = yf.download(pair, interval="15m", period="5d", progress=False)

            if data.empty:
                continue

            close = data["Close"]

            rsi = RSIIndicator(close=close, window=14).rsi()

            last_rsi = rsi.iloc[-1]

            print(pair,"RSI:",round(last_rsi,2))

            if pair not in last_signal:
                last_signal[pair] = "none"

            # OVERSOLD
            if last_rsi < 30 and last_signal[pair] != "buy":

                send_telegram(
f"""
📉 RSI OVERSOLD

PAIR : {pair}
RSI : {round(last_rsi,2)}

Potensi BUY
"""
)

                last_signal[pair] = "buy"

            # OVERBOUGHT
            elif last_rsi > 70 and last_signal[pair] != "sell":

                send_telegram(
f"""
📈 RSI OVERBOUGHT

PAIR : {pair}
RSI : {round(last_rsi,2)}

Potensi SELL
"""
)

                last_signal[pair] = "sell"

            # RESET
            elif 40 < last_rsi < 60:
                last_signal[pair] = "none"

        except Exception as e:

            print("Error:",pair,e)

while True:

    check_rsi()

    time.sleep(60)