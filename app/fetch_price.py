import yfinance as yf


def normalize_stock_id(stock_id: str) -> str:
    """
    台股在 Yahoo Finance 需要加上 .TW
    例如：
    2330 -> 2330.TW
    0050 -> 0050.TW
    """
    stock_id = stock_id.strip()

    if stock_id.endswith(".TW") or stock_id.endswith(".TWO"):
        return stock_id

    return f"{stock_id}.TW"


def fetch_latest_close_price(stock_id: str):
    """
    抓單一股票的最近收盤價
    """

    yahoo_symbol = normalize_stock_id(stock_id)

    ticker = yf.Ticker(yahoo_symbol)

    history = ticker.history(period="5d")

    if history.empty:
        raise ValueError(f"找不到股票資料：{stock_id}")

    latest_row = history.iloc[-1]

    trade_date = history.index[-1].date().isoformat()
    close_price = float(latest_row["Close"])

    return {
        "stock_id": stock_id,
        "yahoo_symbol": yahoo_symbol,
        "trade_date": trade_date,
        "close_price": close_price,
    }

def fetch_historical_close_prices(stock_id: str, period: str = "1y"):
    yahoo_symbol = normalize_stock_id(stock_id)

    ticker = yf.Ticker(yahoo_symbol)

    history = ticker.history(period=period)

    if history.empty:
        raise ValueError(f"找不到歷史股價資料：{stock_id}")

    price_data_list = []

    for trade_date, row in history.iterrows():
        close_price = row["Close"]

        if close_price is None:
            continue

        price_data_list.append({
            "stock_id": stock_id,
            "yahoo_symbol": yahoo_symbol,
            "trade_date": trade_date.date().isoformat(),
            "close_price": float(close_price),
        })

    return price_data_list