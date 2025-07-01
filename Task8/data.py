import yfinance as yf
from datetime import datetime

symbols = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BSE MidCap": "BSE-MIDCAP.BO"
}

for name, symbol in symbols.items():
    print(f"Downloading {name} ({symbol})...")
    data = yf.download(
        tickers=symbol,
        period="1d",
        interval="1m",
        progress=False
    )

    if data.empty:
        print(f" No data found for {name}")
        continue

    filename = f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"
    data.to_csv(filename)
    print(f" Saved: {filename}")
