from yfinance import Ticker
from datetime import datetime, timezone


def fetch_share_price(symbol: str):

    ticker = Ticker(f"{symbol}.NS")

    price = None
    name = None
    try:
        info = ticker.info
        price = info.get("regularMarketPrice")
        name = info.get("longName") or info.get("shortName")
    except:
        pass

    if not price:
        raise ValueError(f"Price not available for symbol {symbol}")

    response = {"name": name, "price": price}
    print(response)
    return {"name": name, "symbol": symbol, "price": price}
