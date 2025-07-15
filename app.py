import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters
import logging

# Настройки
TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + WEBHOOK_PATH

app = FastAPI()
telegram_app = Application.builder().token(TOKEN).build()

# === Твоите хендлъри тук ===
# Пример:
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Здравей и добре дошъл!")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

@app.on_event("startup")
async def startup():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    telegram_app.create_task(telegram_app.initialize())

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
