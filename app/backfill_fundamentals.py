from app.database import (
    initialize_database,
    insert_fundamentals,
    insert_dividends,
)
from app.fetch_fundamental import (
    fetch_recent_fundamentals,
    fetch_latest_dividend,
)
from app.portfolio import get_all_portfolios


def backfill_all_fundamentals():
    initialize_database()

    portfolio_groups = get_all_portfolios()

    for group in portfolio_groups:
        group_name = group["name"]
        portfolio = group["stocks"]

        print(f"\nBackfilling fundamentals group: {group_name}")

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