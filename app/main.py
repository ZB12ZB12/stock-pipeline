from app.database import (
    initialize_database, 
    insert_stock_price
)
from app.fetch_price import fetch_latest_close_price
from app.portfolio import get_all_portfolios
from app.report import build_portfolio_report
from app.google_sheet import update_stock_analysis_sheet

def main():
    print(F"11: initialize_database")
    initialize_database()
    print(F"13: Ending initialize_database\n")

    # portfolio = get_portfolio()
    print(F"16: get_all_portfolios")
    portfolio_groups = get_all_portfolios()
    print(F"18: Ending get_all_portfolios\n")

    for group in portfolio_groups:
        group_name = group["name"]
        portfolio = group["stocks"]

        print(f"\n========== Processing portfolio group: {group_name} ==========")

        for item in portfolio:
            stock_id = item["stock_id"]
            stock_name = item.get("name", "")

            print(f"\n[START] {stock_id} {stock_name}")

            try:
                print(f"[FETCH] Fetching latest close price for {stock_id}...")
                price_data = fetch_latest_close_price(stock_id)
                print(f"[FETCH OK] {price_data}")

            except Exception as e:
                print(f"[FETCH FAILED] stock_id={stock_id}, stock_name={stock_name}")
                print(f"Reason: {repr(e)}")
                continue

            try:
                print(f"[DB] Inserting price data for {stock_id}...")
                insert_stock_price(price_data)
                print(f"[DB OK] Saved {stock_id}")

            except Exception as e:
                print(f"[DB FAILED] stock_id={stock_id}, stock_name={stock_name}")
                print(f"price_data={price_data}")
                print(f"Reason: {repr(e)}")
                continue

        try:
            print(f"\n[REPORT] Building report for group: {group_name}")
            reports = build_portfolio_report(portfolio)
            print(f"[REPORT OK] rows={len(reports)}")

        except Exception as e:
            print(f"[REPORT FAILED] group={group_name}")
            print(f"Reason: {repr(e)}")
            continue

        try:
            print(f"[SHEET] Updating worksheet: {group_name}")
            update_stock_analysis_sheet(
                reports=reports,
                worksheet_title=group_name,
            )
            print(f"[SHEET OK] Updated worksheet: {group_name}")

        except Exception as e:
            print(f"[SHEET FAILED] group={group_name}")
            print(f"Reason: {repr(e)}")
            continue

if __name__ == "__main__":
    main()