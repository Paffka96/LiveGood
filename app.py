import os
from fastapi import FastAPI, Request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import logging

TOKEN = os.environ["BOT_TOKEN"]

WELCOME_TEXT = """
🚀 LiveGood е революционна идея, чието време дойде!

🧬 Това е съвременен поглед към здравето и начина на живот, базиран на достъпни продукти с премиум качество.

👩‍💼 Казвам се Илияна Костадинова и ви каня да станете част от клуба на здрави и успешни хора.

🏆 Аз съм лидер в компанията LiveGood и с радост ви приветствам в моя Telegram бот.

🔍 Тук ще откриете цялата информация за:
✅ нашите качествени продукти
✅ възможността да изградите успешен и печеливш бизнес

💡 Сътрудничеството с LiveGood може да бъде стъпката, която ще промени вашето бъдеще.

❓ Питайте – ще получите пълна информация!
"""

COMPANY_TEXT = (
    "🏢 LiveGood е компания, специализирана в производството и продажбата на премиум хранителни добавки.\n\n"
    "🎯 Нашата мисия е да направим здравето и благосъстоянието достъпни за всички, като предлагаме продукти на разумни цени.\n\n"
    "🌐 В сайта можеш да разгледаш цени както за членове, така и стандартните цени за редовен купувач. След това се върни тук за повече информация. 🙂\n\n"
    "👉 Разгледай сайта оттук: https://livegood.com/ilyyy12"
)

PRODUCTS_TEXT = (
    "🛒 Продукти:\n"
    "• Bio-Active Complete Multi-Vitamin for Men\n"
    "• Bio-Active Multi-Vitamin for Women with Iron\n"
    "• Vitamin D3 and K2\n"
    "• Ultra Magnesium Complex\n"
    "• Complete Plant-Based Protein\n"
    "• Organic Super Greens\n"
    "• Factor4\n"
    "• Daily Essentials Pack\n"
    "• Lean Body Pack\n"
    "• Ultimate Wellness Pack\n"
    "• Skin Care Pack\n"
    "• Maximum Energy Pack\n"
    "• Everything Pack"
)

MARKETING_STEPS = [
    "👋 Добре дошли в LiveGood!\n\nLiveGood е иновационен клуб, създаден, за да ви помогне да водите здравословен начин на живот, използвайки продукти с най-високо качество на достъпни цени.",
    "🤝 Какво е клуб LiveGood?\n\nТова е ексклузивна клубна система, в която можете да получите достъп до най-добрите продукти за здраве с икономия до 75%! Членството струва само $49,95 + $9,95 месечно.",
    "⚙️ Как работи това?\n\n1️⃣ Присъединете се за $49,95.\n2️⃣ Купувайте продукти с отстъпка.\n3️⃣ Споделяйте и печелете!",
    "💸 Възможности за печалба:\n\n✅ Реферален бонус: $25\n✅ Резидуален доход: До $2047,50/месец\n✅ Бонуси за растеж: До 2% от оборота при ранг Diamond!",
    "🌱 Продукти на LiveGood\n\nПроизведени в САЩ – витамини, суперхрани, козметика и др.",
    "🎉 Присъединете се към LiveGood!\n\nНе пропускайте шанса да промените живота си още днес!\n\n🔓 Може да се регистрирате БЕЗПЛАТНО и да се отпишете по всяко време!"
]

SOCIAL_BUTTONS = [
    [InlineKeyboardButton("📘 Facebook", url="https://www.facebook.com/profile.php?id=100024332053965")],
    [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/ipetrova65/")]
]

MAIN_BUTTONS = [
    [InlineKeyboardButton("ℹ️ За компанията", callback_data="company")],
    [InlineKeyboardButton("🧪 Продукти", callback_data="products")],
    [InlineKeyboardButton("📈 Маркетинг", callback_data="marketing_0")],
    [InlineKeyboardButton("📬 Свържете се с мен", callback_data="contact")]
]

# --- Telegram handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("welcome.jpg", "rb") as photo:
            await update.message.reply_photo(photo)
    except Exception as e:
        print("Не можа да изпрати снимката:", e)

    await update.message.reply_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(MAIN_BUTTONS))

    try:
        with open("welcome.mp4", "rb") as video:
            await update.message.reply_video(video)
    except Exception as e:
        print("Не можа да изпрати видеото:", e)
        await update.message.reply_text("🎥 Видео не е намерено или не може да бъде изпратено.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Натиснете бутона по-долу за начало ⬇️",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Старт", callback_data="start")]])
        )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "start":
        try:
            with open("welcome.jpg", "rb") as photo:
                await query.message.reply_photo(photo)
        except Exception as e:
            print("Не можа да изпрати снимката:", e)
        await query.message.reply_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(MAIN_BUTTONS))

        try:
            with open("welcome.mp4", "rb") as video:
                await query.message.reply_video(video)
        except Exception as e:
            print("Не можа да изпрати видеото:", e)
            await query.message.reply_text("🎥 Видео не е намерено или не може да бъде изпратено.")

    elif data == "company":
        await query.edit_message_text(COMPANY_TEXT, reply_markup=InlineKeyboardMarkup(MAIN_BUTTONS))

    elif data == "products":
        await query.edit_message_text(PRODUCTS_TEXT, reply_markup=InlineKeyboardMarkup(MAIN_BUTTONS))

    elif data.startswith("marketing_"):
        step = int(data.split("_")[1])
        buttons = []
        if step > 0:
            buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"marketing_{step - 1}"))
        if step < len(MARKETING_STEPS) - 1:
            buttons.append(InlineKeyboardButton("Напред ➡️", callback_data=f"marketing_{step + 1}"))
        else:
            buttons = [
                InlineKeyboardButton("📝 Регистрирай се безплатно", url="https://livegoodtour.com/ilyyy12"),
                InlineKeyboardButton("📲 Социални мрежи", callback_data="contact")
            ]

        await query.edit_message_text(MARKETING_STEPS[step], reply_markup=InlineKeyboardMarkup([buttons]))

    elif data == "contact":
        combined_buttons = SOCIAL_BUTTONS + MAIN_BUTTONS
        await query.edit_message_text("📞 Свържете се с мен чрез бутоните по-долу 👇", reply_markup=InlineKeyboardMarkup(combined_buttons))

# --- Set up Telegram bot application ---

telegram_app = ApplicationBuilder().token(TOKEN).build()

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(handle_buttons))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# --- FastAPI app ---

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()   # <--- ТУК добави инициализацията

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# --- Run only locally with polling (optional) ---

if __name__ == "__main__":
    print("Започва polling (само за локално ползване)")
    telegram_app.run_polling()
