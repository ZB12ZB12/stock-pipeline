# Stock Pipeline

一個用來更新股票資料，並將資料同步到 Google Sheets 的資料管線專案。

本專案支援兩種執行方式：

- 使用 Docker 執行
- 在本機 Python 環境直接執行

---

## 專案下載

先從 GitHub 下載專案：

```bash
git clone https://github.com/ZB12ZB12/stock-pipeline.git
cd stock-pipeline
```

---

## 必要設定檔

由於部分敏感檔案不會放進 Git，因此 pull 完專案後，需要自行補上以下檔案：

```text
.env
credentials/google_service_account.json
```

### `.env`

請在專案根目錄建立 `.env` 檔案，用來放環境變數。

### `credentials/google_service_account.json`

請將 Google Service Account 的憑證檔放在：

```text
credentials/google_service_account.json
```

此檔案通常用來讓程式可以存取 Google Sheets。

---

## 使用 Docker 執行

### 建立 Docker Image

```bash
docker compose build
```

第一次建立 image 並執行時，也可以直接使用：

```bash
docker compose up --build
```

---

## Docker 常用指令

### 日常更新

```bash
docker compose run --rm stock-pipeline python -m app.main
```

也可以使用簡寫：

```bash
docker compose run --rm stock-pipeline
```

### 補股票歷史資料

```bash
docker compose run --rm stock-pipeline python -m app.backfill_prices
```

---

## 在本機終端機直接執行

如果不是使用 Docker，也可以直接在本機終端機執行 Python 指令。

### 新增股票時

新增股票時，建議先補歷史資料，再執行日常更新：

```bash
python -m app.backfill_prices
python -m app.main
```

### 每天自動更新時

每天自動更新只需要執行：

```bash
python -m app.main
```

---

## 腳本說明

### `app.backfill_prices`

執行指令：

```bash
python -m app.backfill_prices
```

用途：

- 當想要新增一檔股票的數據時，就跑這個腳本
- 既有股票：重新補資料，重複日期會被覆蓋
- 新股票：新增一年歷史資料
- 同一天同一檔股票不會重複新增
- 當想要讓數據跑到 Google Sheets 上時，就跑這個腳本

### `app.main`

執行指令：

```bash
python -m app.main
```

用途：

- 每天自動更新時執行
- 更新目前已設定股票的最新資料

---

## 常見使用情境

### 情境一：第一次啟動專案

```bash
git clone https://github.com/ZB12ZB12/stock-pipeline.git
cd stock-pipeline
```

補上必要設定檔：

```text
.env
credentials/google_service_account.json
```

建立並啟動 Docker：

```bash
docker compose up --build
```

---

### 情境二：新增股票資料

使用 Docker：

```bash
docker compose run --rm stock-pipeline python -m app.backfill_prices
docker compose run --rm stock-pipeline python -m app.main
```

或使用本機 Python：

```bash
python -m app.backfill_prices
python -m app.main
```

---

### 情境三：每日更新資料

使用 Docker：

```bash
docker compose run --rm stock-pipeline python -m app.main
```

或使用本機 Python：

```bash
python -m app.main
```

---

## 指令速查

| 目的 | Docker 指令 | 本機指令 |
| --- | --- | --- |
| 建立 Docker image | `docker compose build` | - |
| 第一次建立並啟動 | `docker compose up --build` | - |
| 日常更新 | `docker compose run --rm stock-pipeline python -m app.main` | `python -m app.main` |
| 補歷史資料 | `docker compose run --rm stock-pipeline python -m app.backfill_prices` | `python -m app.backfill_prices` |
| 新增股票資料 | `docker compose run --rm stock-pipeline python -m app.backfill_prices` | `python -m app.backfill_prices` |

---

## 建議流程

### 開發或測試時

```bash
python -m app.backfill_prices
python -m app.main
```

### 正式或排程執行時

```bash
docker compose run --rm stock-pipeline python -m app.main
```

---

## 注意事項

- `.env` 不應提交到 Git。
- `credentials/google_service_account.json` 不應提交到 Git。
- 若新增股票，請先執行 `app.backfill_prices`。
- 若只是每日更新，執行 `app.main` 即可。
- 若要讓數據跑到 Google Sheets 上，請執行 `app.backfill_prices`。
