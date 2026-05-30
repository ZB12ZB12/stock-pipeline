from app.database import (
    initialize_database, 
    insert_stock_price
)
from app.fetch_price import fetch_latest_close_price
from app.portfolio import get_portfolio
from app.report import build_portfolio_report
from app.google_sheet import update_stock_analysis_sheet

def main():
    initialize_database()

    portfolio = get_portfolio()

    for item in portfolio:
        stock_id = item["stock_id"]

        try:
            stock_price = fetch_latest_close_price(stock_id)
            insert_stock_price(stock_price)

        except Exception as e:
            print(f"Failed: {stock_id}, reason: {e}")

    reports = build_portfolio_report(portfolio)
    update_stock_analysis_sheet(reports)

if __name__ == "__main__":
    main()