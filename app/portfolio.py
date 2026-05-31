import csv
import json
from app.config import PORTFOLIO_CSV_PATH

# PORTFOLIO_CSV_PATH = "data/portfolio_sres5.csv"

# def get_portfolio():
#     portfolio = []

#     with open(PORTFOLIO_CSV_PATH, mode="r", encoding="utf-8-sig") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             stock_id = row["stock_id"].strip()
#             stock_name = row["stock_name"].strip()
#             print(F"get stock (portfolio.py): {stock_name}")
#             shares = int(row["shares"])

#             if stock_id:
#                 portfolio.append({
#                     "stock_id": stock_id,
#                     "stock_name": stock_name,
#                     "shares": shares,
#                 })

#     return portfolio


# def get_stock_ids():
#     portfolio = get_portfolio()

#     return [item["stock_id"] for item in portfolio]

PORTFOLIO_CONFIG_PATH = "config/portfolios.json"

def load_portfolio_configs():
    with open(PORTFOLIO_CONFIG_PATH, mode="r", encoding="utf-8") as file:
        return json.load(file)


def get_portfolio_from_file(portfolio_file: str):
    portfolio = []

    with open(portfolio_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            stock_id = row["stock_id"].strip()
            stock_name = row["stock_name"].strip()
            shares = int(row.get("shares", 0))

            print(f"get stock (portfolio.py): {stock_name}")

            if stock_id:
                portfolio.append({
                    "stock_id": stock_id,
                    "stock_name": stock_name,
                    "shares": shares,
                })

    return portfolio


def get_all_portfolios():
    configs = load_portfolio_configs()

    portfolios = []

    for portfolio_key, config in configs.items():
        portfolios.append({
            "key": portfolio_key,
            "name": config["name"],
            "file": config["file"],
            "stocks": get_portfolio_from_file(config["file"]),
        })

    return portfolios