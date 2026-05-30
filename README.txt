先 python -m venv stock-pipeline，建立虛擬環境

-

建立 image 並執行：docker compose up --build

之後要手動跑：docker compose run --rm stock-pipeline

補資料腳本也用 Docker 跑：docker compose run --rm stock-pipeline python -m app.backfill_prices

日常更新：docker compose run --rm stock-pipeline python -m app.main

-

新增股票時：
python -m app.backfill_prices
python -m app.main

每天自動更新時，只需要：
python -m app.main

-

python -m app.backfill_prices
    => 當想要新增一檔股票的數據時，就跑這個腳本
        => 既有股票：重新補資料，重複日期會被覆蓋
        => 新股票：新增一年歷史資料
        => 同一天同一檔不會重複新增
python -m app.backfill_prices
    => 當想要讓數據跑到 google sheet 上時，就跑這個腳本