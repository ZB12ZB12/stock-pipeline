import sqlite3
from app.config import DB_PATH


def get_connection():
    """
    建立 SQLite 連線
    """
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    建立資料表
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_id TEXT NOT NULL,
        yahoo_symbol TEXT NOT NULL,
        trade_date DATE NOT NULL,
        close_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(stock_id, trade_date)
    )
    """) # UNIQUE(stock_id, trade_date): 同一檔股票一天只會有一筆資料

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_fundamentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_id TEXT NOT NULL,
        report_date DATE NOT NULL,
        eps REAL,
        gross_margin REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(stock_id, report_date)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_dividends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_id TEXT NOT NULL,
        year INTEGER NOT NULL,
        cash_dividend REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(stock_id, year)
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized.")


def insert_stock_price(price_data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO stock_prices (
        stock_id,
        yahoo_symbol,
        trade_date,
        close_price
    )
    VALUES (?, ?, ?, ?)
    """, (
        price_data["stock_id"],
        price_data["yahoo_symbol"],
        price_data["trade_date"],
        price_data["close_price"],
    ))

    conn.commit()
    conn.close()

    print(
        f"Saved: {price_data['stock_id']} "
        f"{price_data['trade_date']} "
        f"{price_data['close_price']}"
    )
    return


def insert_stock_prices(price_data_list: list[dict]):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT OR REPLACE INTO stock_prices (
        stock_id,
        yahoo_symbol,
        trade_date,
        close_price
    )
    VALUES (?, ?, ?, ?)
    """, [
        (
            item["stock_id"],
            item["yahoo_symbol"],
            item["trade_date"],
            item["close_price"],
        )
        for item in price_data_list
    ])

    conn.commit()
    conn.close()

    print(f"Saved {len(price_data_list)} price records.")
    return


def get_all_stock_prices():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        stock_id,
        yahoo_symbol,
        trade_date,
        close_price,
        created_at
    FROM stock_prices
    ORDER BY trade_date DESC, stock_id ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def insert_fundamentals(fundamental_data_list: list[dict]):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT OR REPLACE INTO stock_fundamentals (
        stock_id,
        report_date,
        eps,
        gross_margin
    )
    VALUES (?, ?, ?, ?)
    """, [
        (
            item["stock_id"],
            item["report_date"],
            item.get("eps"),
            item.get("gross_margin"),
        )
        for item in fundamental_data_list
    ])

    conn.commit()
    conn.close()

    print(f"Saved {len(fundamental_data_list)} fundamental records.")


def insert_dividends(dividend_data_list: list[dict]):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT OR REPLACE INTO stock_dividends (
        stock_id,
        year,
        cash_dividend
    )
    VALUES (?, ?, ?)
    """, [
        (
            item["stock_id"],
            item["year"],
            item.get("cash_dividend"),
        )
        for item in dividend_data_list
    ])

    conn.commit()
    conn.close()

    print(f"Saved {len(dividend_data_list)} dividend records.")


def get_recent_fundamentals(stock_id: str, limit: int = 4):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        report_date,
        eps,
        gross_margin
    FROM stock_fundamentals
    WHERE stock_id = ?
    ORDER BY report_date DESC
    LIMIT ?
    """, (stock_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_latest_dividend(stock_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        year,
        cash_dividend
    FROM stock_dividends
    WHERE stock_id = ?
    ORDER BY year DESC
    LIMIT 1
    """, (stock_id,))

    row = cursor.fetchone()
    conn.close()

    return row