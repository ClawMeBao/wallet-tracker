from typing import List, Dict
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_client(creds_path: str) -> gspread.Client:
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    return gspread.authorize(creds)


def append_rows(creds_path: str, sheet_id: str, rows: List[List]):
    gc = get_client(creds_path)
    sh = gc.open_by_key(sheet_id)
    ws = sh.sheet1
    ws.append_rows(rows, value_input_option="USER_ENTERED")


def ensure_headers(creds_path: str, sheet_id: str):
    gc = get_client(creds_path)
    sh = gc.open_by_key(sheet_id)
    ws = sh.sheet1
    headers = ws.row_values(1)
    expected = ["timestamp", "chain", "address", "token", "amount", "usd"]
    if headers != expected:
        ws.clear()
        ws.append_row(expected)
