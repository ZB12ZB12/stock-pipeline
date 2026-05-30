from dotenv import load_dotenv
import os

load_dotenv()

# 舊版: DB_PATH = os.getenv("DB_PATH", "data/stocks.db")
DB_PATH = os.getenv("DB_PATH")

GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")

GOOGLE_CREDENTIAL_FILE = os.getenv(
    "GOOGLE_CREDENTIAL_FILE"
)