import asyncio
from io import BytesIO
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .state import StateStore


def format_summary(summary: dict) -> str:
    if not summary:
        return "Chưa có dữ liệu."
    lines = ["Danh mục (USD):"]
    total = 0
    for token, usd in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- {token.upper()}: ${usd:,.2f}")
        total += usd
    lines.append(f"Tổng: ${total:,.2f}")
    return "\n".join(lines)


def build_app(bot_token: str, state: StateStore, output_csv_path: str, run_once: Callable, stop_event: asyncio.Event) -> Application:
    app = Application.builder().token(bot_token).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bot sẵn sàng. Dùng /add, /remove, /list, /set_interval, /report, /chart, /download")

    async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /add <chain> <address>")
            return
        chain, address = context.args[0], context.args[1]
        ok = state.add_wallet(chain, address)
        if ok:
            await update.message.reply_text("Đã thêm")
        else:
            await update.message.reply_text("Đã tồn tại")

    async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: /remove <address>")
            return
        address = context.args[0]
        ok = state.remove_wallet(address)
        if ok:
            await update.message.reply_text("Đã xóa")
        else:
            await update.message.reply_text("Không tìm thấy")

    async def list_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not state.state.wallets:
            await update.message.reply_text("Chưa có ví")
            return
        lines = [f"- {w.chain}: {w.address}" for w in state.state.wallets]
        await update.message.reply_text("\n".join(lines))

    async def set_interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: /set_interval <minutes>")
            return
        try:
            minutes = int(context.args[0])
            state.set_interval(minutes)
            await update.message.reply_text(f"Đặt chu kỳ {minutes} phút")
        except ValueError:
            await update.message.reply_text("Giá trị không hợp lệ")

    async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
        res = await run_once()
        await update.message.reply_text(format_summary(res.get("summary", {})))

    async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
        res = await run_once()
        summary = res.get("summary", {})
        if not summary:
            await update.message.reply_text("Chưa có dữ liệu")
            return
        labels = list(summary.keys())
        sizes = [summary[k] for k in labels]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%")
        ax.axis('equal')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        await update.message.reply_photo(buf)
        plt.close(fig)

    async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
        path = Path(output_csv_path)
        if not path.exists():
            await update.message.reply_text("Chưa có file CSV")
            return
        await update.message.reply_document(document=path.open("rb"), filename=path.name)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("list", list_wallets))
    app.add_handler(CommandHandler("set_interval", set_interval))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("chart", chart))
    app.add_handler(CommandHandler("download", download))
    return app
