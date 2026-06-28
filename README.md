# 高點的bug還沒修正完成，還沒讓4個高點顯示出來

# Stock Pipeline

一個用來收集台股資料、儲存至 SQLite，並同步更新 Google Sheets 的股票資料管線專案。

目前支援：

* 每日收盤價
* 最近 5 個交易日價格
* 歷史高點
* 一年高點
* 半年高點
* 三個月高點
* 一個月高點
* 最近 4 季 EPS
* 最近 4 季毛利率
* 最近年度配息
* Google Sheets 自動同步

---

# 專案架構

```text
stock-pipeline/
│
├─ app/
│  ├─ main.py
│  ├─ backfill_prices.py
│  ├─ backfill_fundamentals.py
│  ├─ fetch_price.py
│  ├─ fetch_fundamental.py
│  ├─ portfolio.py
│  ├─ database.py
│  ├─ report.py
│  ├─ google_sheet.py
│  └─ config.py
│
├─ data/
│  ├─ portfolio.csv
│  └─ stocks.db
│
├─ credentials/
│  └─ google_service_account.json
│
├─ .env
├─ .env.example
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```

---

# 專案下載與環境建置

```bash
# 從 github 拉檔案下來
git clone https://github.com/ZB12ZB12/stock-pipeline.git

# 切換到專案根目錄
cd stock-pipeline

# 建立虛擬環境，並將所有需要的套件裝好
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# 必要設定檔

由於部分敏感檔案不會放入 Git Repository，因此下載專案後需自行補上：

```text
.env
credentials/google_service_account.json
```

---

## .env

範例：

```env
DB_PATH=data/stocks.db

GOOGLE_SHEET_NAME=股票分析

GOOGLE_CREDENTIAL_FILE=credentials/google_service_account.json

FINMIND_TOKEN=
```

---

## Google Service Account

請將：

```text
google_service_account.json
```

放置於：

```text
credentials/google_service_account.json
```

---

# 使用 Docker

## 建立 Image

```bash
docker compose build
```

---

## 第一次建立並執行

```bash
docker compose up --build
```

---

## 日常更新與補檔

* **日常更新**：
  ```bash
  docker compose run --rm stock-pipeline python -m app.main
  ```
  *(或直接執行 `docker compose run --rm stock-pipeline` 也可以)*

* **補資料腳本**：
  ```bash
  docker compose run --rm stock-pipeline python -m app.backfill_prices
  ```

---

# 本機執行

## 執行流程

* **新增股票時**，請依序執行以下指令：
  ```bash
  python -m app.backfill_fundamentals
  python -m app.backfill_prices
  python -m app.main
  ```

* **日常自動更新時**，只需要執行：
  ```bash
  python -m app.main
  ```

---

## 腳本詳細說明

### 1. 補股價歷史資料 (`python -m app.backfill_prices`)
當想要新增或重新讀取股票的數據時，就跑這個腳本：
* **既有股票**：重新補資料，重複日期會被覆蓋。
* **新股票**：新增一年歷史資料。
* **重複性防範**：同一天同一檔股票不會重複新增。

### 2. 補基本面資料 (`python -m app.backfill_fundamentals`)
當想要更新或補齊基本面資料時執行：
* 補最近 4 季 EPS
* 補最近 4 季毛利率
* 補最近年度配息

### 3. 日常更新與同步 (`python -m app.main`)
當想要讓最新的收盤數據與報表同步到 Google Sheets 上時，就跑這個腳本：
* 更新最新收盤價，儲存至 SQLite，並自動同步更新至 Google Sheets。

---

# Google Sheet 資料內容

目前會同步以下資料：

```text
持有股數

最近四季 EPS
最近四季毛利率

最近年度配息

歷史高點
一年高點
半年高點
三個月高點
一個月高點

最近五個交易日收盤價
```

---

# SQLite 資料表

## stock_prices

儲存每日收盤價：

```text
stock_id
trade_date
close_price
```

---

## stock_fundamentals

儲存基本面資料：

```text
stock_id
report_date
eps
gross_margin
```

---

## stock_dividends

儲存股利資料：

```text
stock_id
year
cash_dividend
```

---

# 常見操作

## 新增股票

修改：

```text
data/portfolio/<自定義的類股>.csv
```

新增股票後執行：

```bash
python -m app.backfill_fundamentals
python -m app.backfill_prices
python -m app.main
```

或 Docker：

```bash
docker compose run --rm stock-pipeline python -m app.backfill_fundamentals

docker compose run --rm stock-pipeline python -m app.backfill_prices

docker compose run --rm stock-pipeline python -m app.main
```

---

## 每日更新

```bash
python -m app.main
```

或：

```bash
docker compose run --rm stock-pipeline python -m app.main
```

---

# 注意事項

* `.env` 不應提交至 Git。
* `credentials/google_service_account.json` 不應提交至 Git。
* `stocks.db` 不應提交至 Git。
* 新增股票時建議先執行：

  * `app.backfill_fundamentals`
  * `app.backfill_prices`
* 日常更新只需執行：

  * `app.main`
* Google Sheet 更新由 `app.main` 負責。