from app.database import (
    initialize_database,
    insert_fundamentals,
    insert_dividends,
)
from app.fetch_fundamental import (
    fetch_recent_fundamentals,
    fetch_latest_dividend,
)
from app.portfolio import get_portfolio


def backfill_all_fundamentals():
    initialize_database()

    portfolio = get_portfolio()

    for item in portfolio:
        stock_id = item["stock_id"]

        try:
            print(f"Backfilling fundamentals: {stock_id}")

            fundamentals = fetch_recent_fundamentals(stock_id)
            insert_fundamentals(fundamentals)

            dividends = fetch_latest_dividend(stock_id)
            insert_dividends(dividends)

            print(f"Done: {stock_id}")

        except Exception as e:
            print(f"Failed: {stock_id}, reason: {e}")


if __name__ == "__main__":
    backfill_all_fundamentals()