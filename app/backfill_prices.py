from app.database import initialize_database, insert_stock_prices
from app.fetch_price import fetch_historical_close_prices
from app.portfolio import get_portfolio


def backfill_all_stocks(period: str = "1y"):
    initialize_database()

    portfolio = get_portfolio()
    print(F"(backfill_prices.py)")

    for item in portfolio:
        stock_id = item["stock_id"]

        try:
            print(f"Backfilling {stock_id}...")

            price_data_list = fetch_historical_close_prices(
                stock_id=stock_id,
                period=period,
            )

            insert_stock_prices(price_data_list)

            print(f"Done: {stock_id}")

        except Exception as e:
            print(f"Failed: {stock_id}, reason: {e}")


if __name__ == "__main__":
    backfill_all_stocks(period="1y")