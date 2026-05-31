from app.database import (
    initialize_database, 
    insert_stock_price
)
from app.fetch_price import fetch_latest_close_price
from app.portfolio import get_all_portfolios
from app.report import build_portfolio_report
from app.google_sheet import update_stock_analysis_sheet

def main():
    initialize_database()

    # portfolio = get_portfolio()
    portfolio_groups = get_all_portfolios()

    for group in portfolio_groups:
        group_name = group["name"]
        portfolio = group["stocks"]

        print(f"\nProcessing portfolio group: {group_name}")

        for item in portfolio:
            stock_id = item["stock_id"]

            try:
                price_data = fetch_latest_close_price(stock_id)
                insert_stock_price(price_data)

            except Exception as e:
                print(f"Failed: {stock_id}, reason: {e}")

        reports = build_portfolio_report(portfolio)

        update_stock_analysis_sheet(
            reports=reports,
            worksheet_title=group_name,
        )

if __name__ == "__main__":
    main()