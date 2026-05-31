import re
from datetime import date, timedelta
import requests
from app.config import FINMIND_TOKEN


FINMIND_API_URL = "https://api.finmindtrade.com/api/v4/data"


def parse_tw_year(value):
    """
    把台灣民國年格式轉成西元年。
    例如：
    113年 -> 2024
    113年第4季 -> 2024
    """
    if value is None:
        return None

    text = str(value)

    match = re.search(r"(\d+)", text)

    if not match:
        return None

    tw_year = int(match.group(1))

    return tw_year + 1911


def fetch_finmind_data(dataset: str, stock_id: str, start_date: str):
    params = {
        "dataset": dataset,
        "data_id": stock_id,
        "start_date": start_date,
    }

    headers = {}

    if FINMIND_TOKEN:
        headers["Authorization"] = f"Bearer {FINMIND_TOKEN}"

    response = requests.get(
        FINMIND_API_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if result.get("status") != 200:
        raise ValueError(f"FinMind API error: {result}")

    return result.get("data", [])


def fetch_recent_fundamentals(stock_id: str):
    """
    抓 EPS 與毛利率。

    FinMind 的 TaiwanStockFinancialStatements 是長表：
    每一列是一個 type，例如 EPS、GrossProfit、Revenue。
    毛利率 = GrossProfit / Revenue * 100
    """

    start_date = (date.today() - timedelta(days=365)).isoformat()

    data = fetch_finmind_data(
        dataset="TaiwanStockFinancialStatements",
        stock_id=stock_id,
        start_date=start_date,
    )

    by_date = {}

    for item in data:
        report_date = item["date"]
        item_type = item["type"]
        value = item["value"]

        if report_date not in by_date:
            by_date[report_date] = {
                "stock_id": stock_id,
                "report_date": report_date,
                "eps": None,
                "gross_profit": None,
                "revenue": None,
                "gross_margin": None,
            }

        if item_type == "EPS":
            by_date[report_date]["eps"] = float(value)

        elif item_type == "GrossProfit":
            by_date[report_date]["gross_profit"] = float(value)

        elif item_type in ["Revenue", "OperatingRevenue"]:
            by_date[report_date]["revenue"] = float(value)

    results = []

    for report_date, row in by_date.items():
        gross_profit = row["gross_profit"]
        revenue = row["revenue"]

        if gross_profit is not None and revenue not in [None, 0]:
            row["gross_margin"] = gross_profit / revenue * 100

        if row["eps"] is not None or row["gross_margin"] is not None:
            results.append({
                "stock_id": stock_id,
                "report_date": report_date,
                "eps": row["eps"],
                "gross_margin": row["gross_margin"],
            })

    results.sort(key=lambda x: x["report_date"], reverse=True)

    return results[:4]


def fetch_latest_dividend(stock_id: str):
    """
    抓最近年度現金股利。
    """

    start_date = (date.today() - timedelta(days=365)).isoformat()

    data = fetch_finmind_data(
        dataset="TaiwanStockDividend",
        stock_id=stock_id,
        start_date=start_date,
    )

    dividends = []

    for item in data:
        year = parse_tw_year(item.get("year"))
        cash_dividend = (
            item.get("CashEarningsDistribution")
            or item.get("cash_dividend")
            or item.get("CashDividend")
        )

        if year is None or cash_dividend is None:
            continue

        dividends.append({
            "stock_id": stock_id,
            "year": year,
            "cash_dividend": float(cash_dividend),
        })

    dividends.sort(key=lambda x: x["year"], reverse=True)

    return dividends[:1]