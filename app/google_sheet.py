import gspread
from google.oauth2.service_account import Credentials

from app.config import GOOGLE_CREDENTIAL_FILE, GOOGLE_SHEET_NAME, YEARS


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_google_sheet():
    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDENTIAL_FILE,
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    sheet = client.open(GOOGLE_SHEET_NAME)

    return sheet


def update_stock_prices_to_sheet(rows):
    sheet = get_google_sheet()
    worksheet = sheet.sheet1

    values = [
        ["股票代號", "Yahoo代號", "交易日期", "收盤價", "建立時間"]
    ]

    # print(F"LINE34, rows: {rows}\n")
    for row in rows:
        # print(F"LINE36, row: {row}\n")
        values.append([
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
        ])

    worksheet.clear()

    worksheet.update(
        "A1",
        values
    )

    print("Google Sheet updated.")


def format_price(value):
    if value is None:
        return ""

    return round(float(value), 1)


def format_quarter_label(report_date: str, metric_name: str):
    year = report_date[:4]
    month = int(report_date[5:7])

    if month <= 3:
        quarter = "Q1"
    elif month <= 6:
        quarter = "Q2"
    elif month <= 9:
        quarter = "Q3"
    else:
        quarter = "Q4"

    return f"{year}{quarter} {metric_name}"


# def update_stock_analysis_sheet(reports: list[dict]):
def update_stock_analysis_sheet(reports: list[dict], worksheet_title: str = "股票分析"):
    sheet = get_google_sheet()

    # worksheet_title = "股票分析"

    try:
        worksheet = sheet.worksheet(worksheet_title)
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(
            title=worksheet_title,
            rows=100,
            cols=50
        )

    values = []

    # 第一列：股票名稱
    header = ["指標"]
    for report in reports:
        header.append(f"{report['stock_id']} {report['stock_name']}")
    values.append(header)

    # 收集所有股票最近 4 季的 report_date
    quarter_dates = []

    for report in reports:
        fundamentals = report.get("fundamentals", [])

        for report_date, eps, gross_margin in fundamentals:
            if report_date not in quarter_dates:
                quarter_dates.append(report_date)

    # 只取最近 4 季，但輸出時由舊到新
    quarter_dates = sorted(quarter_dates, reverse=True)[:YEARS* 4]
    quarter_dates = sorted(quarter_dates)

    # EPS：由舊到新
    for report_date in quarter_dates:
        row = [format_quarter_label(report_date, "EPS")]

        for report in reports:
            fundamental_map = {
                item[0]: item
                for item in report.get("fundamentals", [])
            }

            item = fundamental_map.get(report_date)

            if item:
                _, eps, gross_margin = item
                row.append(format_price(eps))
            else:
                row.append("")

        values.append(row)

    # 毛利率：由舊到新
    for report_date in quarter_dates:
        row = [format_quarter_label(report_date, "毛利率")]

        for report in reports:
            fundamental_map = {
                item[0]: item
                for item in report.get("fundamentals", [])
            }

            item = fundamental_map.get(report_date)

            if item:
                _, eps, gross_margin = item

                if gross_margin is not None:
                    row.append(f"{gross_margin:.1f}%")
                else:
                    row.append("")
            else:
                row.append("")

        values.append(row)
    # 本年度 / 最近年度配息
    dividend_year = None

    for report in reports:
        latest_dividend = report.get("latest_dividend")

        if latest_dividend:
            dividend_year = latest_dividend[0]
            break

    if dividend_year:
        row = [f"{dividend_year} 配息"]
    else:
        row = ["配息"]
    
    for report in reports:
        latest_dividend = report.get("latest_dividend")

        if latest_dividend:
            year, cash_dividend = latest_dividend
            row.append(format_price(cash_dividend))
        else:
            row.append("")

    values.append(row)

    # 固定指標列：基本資料
    rows = [
        ("持有股數", "shares"),
        ("歷史高點", "all_time_high"),
        ("一年高點", "one_year_high"),
        ("半年高點", "six_month_high"),
        ("三個月高點", "three_month_high"),
        ("一個月高點", "one_month_high"),
    ]

    for label, key in rows:
        row = [label]
        for report in reports:
            value = report.get(key, "")
            if key == "shares":
                row.append(value)
            else:
                row.append(format_price(value))
        values.append(row)

    # 收集所有最近 5 日日期
    recent_dates = []

    for report in reports:
        for trade_date, close_price in report.get("recent_prices", []):
            if trade_date not in recent_dates:
                recent_dates.append(trade_date)

    recent_dates = sorted(recent_dates, reverse=True)[:5]

    # 建立日期列：第一欄是日期，後面每檔股票只放價格
    for trade_date in recent_dates:
        row = [trade_date]

        for report in reports:
            price_map = {
                date: price
                for date, price in report.get("recent_prices", [])
            }

            close_price = price_map.get(trade_date)

            row.append(format_price(close_price))

        values.append(row)

    worksheet.clear()
    worksheet.update("A1", values)

    print("股票分析工作表已更新。")