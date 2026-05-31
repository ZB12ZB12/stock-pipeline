import yfinance as yf


def get_yahoo_symbols(stock_id: str):
    stock_id = stock_id.strip()

    if stock_id.endswith(".TW") or stock_id.endswith(".TWO"):
        return [stock_id]

    return [
        f"{stock_id}.TW",
        f"{stock_id}.TWO",
    ]


def fetch_latest_close_price(stock_id: str):
    last_error = None

    for yahoo_symbol in get_yahoo_symbols(stock_id):
        try:
            ticker = yf.Ticker(yahoo_symbol)
            history = ticker.history(period="5d")

            if history.empty:
                raise ValueError(f"No data for {yahoo_symbol}")

            latest_row = history.iloc[-1]

            return {
                "stock_id": stock_id,
                "yahoo_symbol": yahoo_symbol,
                "trade_date": history.index[-1].date().isoformat(),
                "close_price": float(latest_row["Close"]),
            }

        except Exception as e:
            last_error = e

    raise ValueError(f"找不到股票資料：{stock_id}, last_error={last_error}")


def fetch_historical_close_prices(stock_id: str, period: str = "1y"):
    last_error = None

    for yahoo_symbol in get_yahoo_symbols(stock_id):
        try:
            ticker = yf.Ticker(yahoo_symbol)
            history = ticker.history(period=period)

            if history.empty:
                raise ValueError(f"No historical data for {yahoo_symbol}")

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

        except Exception as e:
            last_error = e

    raise ValueError(f"找不到歷史股價資料：{stock_id}, last_error={last_error}")