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