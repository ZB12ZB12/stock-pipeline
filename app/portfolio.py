import csv

PORTFOLIO_CSV_PATH = "data/portfolio.csv"

def get_portfolio():
    portfolio = []

    with open(PORTFOLIO_CSV_PATH, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            stock_id = row["stock_id"].strip()
            stock_name = row["stock_name"].strip()
            shares = int(row["shares"])

            if stock_id:
                portfolio.append({
                    "stock_id": stock_id,
                    "stock_name": stock_name,
                    "shares": shares,
                })

    return portfolio


def get_stock_ids():
    portfolio = get_portfolio()

    return [item["stock_id"] for item in portfolio]