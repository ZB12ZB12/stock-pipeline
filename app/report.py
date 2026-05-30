from datetime import date, timedelta

from app.database import get_connection


def get_recent_prices(stock_id: str, limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        trade_date,
        close_price
    FROM stock_prices
    WHERE stock_id = ?
    ORDER BY trade_date DESC
    LIMIT ?
    """, (stock_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_high_price(stock_id: str, start_date: str | None = None):
    conn = get_connection()
    cursor = conn.cursor()

    if start_date:
        cursor.execute("""
        SELECT
            MAX(close_price)
        FROM stock_prices
        WHERE stock_id = ?
          AND trade_date >= ?
        """, (stock_id, start_date))
    else:
        cursor.execute("""
        SELECT
            MAX(close_price)
        FROM stock_prices
        WHERE stock_id = ?
        """, (stock_id,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def build_stock_report(stock_id: str):
    today = date.today()

    one_year_ago = (today - timedelta(days=365)).isoformat()
    six_months_ago = (today - timedelta(days=183)).isoformat()
    three_months_ago = (today - timedelta(days=90)).isoformat()
    one_month_ago = (today - timedelta(days=30)).isoformat()

    return {
        "stock_id": stock_id,
        "recent_prices": get_recent_prices(stock_id, limit=5),
        "all_time_high": get_high_price(stock_id),
        "one_year_high": get_high_price(stock_id, one_year_ago),
        "six_month_high": get_high_price(stock_id, six_months_ago),
        "three_month_high": get_high_price(stock_id, three_months_ago),
        "one_month_high": get_high_price(stock_id, one_month_ago),
    }


def build_portfolio_report(portfolio: list[dict]):
    reports = []

    for item in portfolio:
        stock_id = item["stock_id"]

        report = build_stock_report(stock_id)

        report["stock_name"] = item["stock_name"]
        report["shares"] = item["shares"]

        reports.append(report)

    return reports