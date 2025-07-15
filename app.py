"""
Flask‑based Telegram bot using webhook for free Render Web Service
===============================================================
• Place this file at the project root (same level as requirements.txt).
• Requirements (add to requirements.txt):
    python-telegram-bot==21
    flask
• In Render → Web Service set environment variable BOT_TOKEN with your bot token.
• Start command example (Render → Settings → Start Command):
    gunicorn -w 1 -k gevent app:app
  or simply:
    python app.py
  Render will expose the port set in the PORT env var.
"""

import os
import asyncio

from flask import Flask, request, abort
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Import your existing handlers from telegram_bot.py ===
# Make sure the file name and function names match!
from telegram_bot import start, message_handler, handle_buttons  # noqa: E402

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TOKEN: str | None = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is not set!")

# Render autoinjects PORT; default to 5000 for local dev
PORT: int = int(os.environ.get("PORT", 5000))

# Render gives your public URL via RENDER_EXTERNAL_URL; fallback to manual
PUBLIC_URL: str | None = os.environ.get("RENDER_EXTERNAL_URL")
if not PUBLIC_URL:
    # ✏️ Replace with your Render service URL the first time you deploy,
    # e.g. "https://livegood-bot.onrender.com"
    PUBLIC_URL = "https://<YOUR_RENDER_DOMAIN>.onrender.com"

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{PUBLIC_URL}{WEBHOOK_PATH}"

# ---------------------------------------------------------------------------
# Initialise Flask and PTB Application
# ---------------------------------------------------------------------------
flask_app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

# ↳ Register the same handlers you used with run_polling()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(handle_buttons))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))


# ---------------------------------------------------------------------------
# Webhook route
# ---------------------------------------------------------------------------
@flask_app.post(WEBHOOK_PATH)
def telegram_webhook():
    """Receive updates from Telegram and hand them to PTB."""
    if request.headers.get("Content-Type") != "application/json":
        abort(403)

    update_json = request.get_json(force=True, silent=True)
    if not update_json:
        abort(400)

    update = Update.de_json(update_json, telegram_app.bot)

    # PTB 21 is fully asyncio – delegate the update into the event loop.
    asyncio.create_task(telegram_app.process_update(update))

    return "OK", 200


# ---------------------------------------------------------------------------
# Helper: set webhook once Flask starts (only first time)
# ---------------------------------------------------------------------------
@flask_app.before_first_request
def init_webhook() -> None:
    """Set the webhook to Render public URL (idempotent)."""
    # Delete previous webhook (ignore errors if not set)
    asyncio.run(telegram_app.bot.delete_webhook(drop_pending_updates=True))
    # Set new webhook
    asyncio.run(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
    print(f"✅ Webhook set to {WEBHOOK_URL}")


# ---------------------------------------------------------------------------
# Local dev / Render entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🌐 Starting Flask server with webhook …")
    flask_app.run(host="0.0.0.0", port=PORT)
