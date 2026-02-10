# Wallet Tracker

Dịch vụ theo dõi số dư ví qua Ankr Advanced API, ghi log vào Google Sheets và tương tác qua Telegram bot.

## Tính năng
- Thêm/xóa ví theo dõi qua Telegram.
- Đặt chu kỳ chạy (testing: 5 phút, production: 6h; có thể thay đổi qua bot).
- Lấy số dư token và quy đổi USD (Ankr). Nếu thiếu giá sẽ bổ sung nhà cung cấp giá khác.
- Lưu kết quả vào Google Sheets.
- Báo cáo/biểu đồ danh mục qua Telegram.

## Cấu hình
Sao chép `.env.example` thành `.env` và điền:
```
TELEGRAM_BOT_TOKEN=...
ANKR_API_KEY=...
SHEET_ID=...
SHEETS_CREDENTIALS_PATH=./credentials.json
LOG_LEVEL=INFO
TRACK_INTERVAL_MINUTES=5
PROD_INTERVAL_MINUTES=360
STATE_PATH=./data/state.json
```

- `credentials.json`: file service account có quyền edit Google Sheet (không commit). Hoặc để ngoài repo và chỉnh đường dẫn.
- Không commit token/API key.

## Chạy cục bộ
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

## Docker
```
docker build -t wallet-tracker .
docker run --rm \
  -e TELEGRAM_BOT_TOKEN=... \
  -e ANKR_API_KEY=... \
  -e SHEET_ID=... \
  -e SHEETS_CREDENTIALS_PATH=/app/credentials.json \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  wallet-tracker
```

## Cấu trúc
- `src/config.py` — load env.
- `src/state.py` — lưu ví, chu kỳ.
- `src/ankr_client.py` — wrapper Ankr.
- `src/pricing.py` — quy đổi giá USD.
- `src/sheets.py` — ghi Google Sheets.
- `src/tracker.py` — logic periodic.
- `src/bot.py` — Telegram handlers.
- `src/main.py` — entrypoint.

## Lưu ý bảo mật
- Không lưu khóa trong code. Dùng env/volume.
- Đảm bảo token bot, Ankr key, credentials Google chỉ cung cấp qua env/volume.
