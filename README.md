# Wallet Tracker

Dịch vụ theo dõi số dư ví qua Ankr Advanced API, ghi log vào file CSV local và tương tác qua Telegram bot.

## Tính năng
- Thêm/xóa ví theo dõi qua Telegram.
- Đặt chu kỳ chạy (testing: 5 phút, production: 6h; có thể thay đổi qua bot).
- Lấy số dư token và quy đổi USD (Ankr). Nếu thiếu giá sẽ bổ sung nhà cung cấp giá khác.
- Lưu kết quả vào file CSV local.
- Báo cáo/biểu đồ danh mục qua Telegram, tải CSV qua bot.

## Cấu hình
Sao chép `.env.example` thành `.env` và điền:
```
TELEGRAM_BOT_TOKEN=...
ANKR_API_KEY=...
LOG_LEVEL=INFO
TRACK_INTERVAL_MINUTES=5
PROD_INTERVAL_MINUTES=360
STATE_PATH=./data/state.json
OUTPUT_CSV_PATH=./data/balances.csv
```

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
  -e OUTPUT_CSV_PATH=/app/data/balances.csv \
  -v $(pwd)/data:/app/data \
  wallet-tracker
```

## Cấu trúc
- `src/config.py` — load env.
- `src/state.py` — lưu ví, chu kỳ.
- `src/ankr_client.py` — wrapper Ankr.
- `src/pricing.py` — quy đổi giá USD.
- `src/tracker.py` — logic periodic + ghi CSV.
- `src/bot.py` — Telegram handlers (report/chart/download CSV).
- `src/main.py` — entrypoint.

## Lưu ý bảo mật
- Không lưu khóa trong code. Dùng env/volume cho token bot, Ankr key.
