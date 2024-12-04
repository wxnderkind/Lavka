import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
import requests
import json

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (замени на свой)
BOT_TOKEN = '7540557414:AAEqUjCnuerTAjRolMTk_pOdRZjct42r8Yw'

# URL Mini App
MINI_APP_URL = 'https://wxnderkind.github.io/Lavka/'

# Пример данных о продуктах (можно заменить на динамическое получение из базы данных)
PRODUCTS = [
    {
        "name": "ChatGPT Plus",
        "variations": [
            {"name": "ChatGPT Plus | Personal Account", "price": "2500 RUB", "quantity": "123 pcs."},
            {"name": "ChatGPT Plus | Public Account", "price": "599 RUB", "quantity": "123 pcs."},
            {"name": "ChatGPT Account", "price": "89 RUB", "quantity": "123 pcs."},
        ]
    },
    # Добавь больше продуктов по аналогии
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton(
                "Открыть магазин",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Добро пожаловать в магазин **Lavka**. Нажми кнопку ниже, чтобы начать покупки.",
        reply_markup=reply_markup
    )

# Обработка данных из Web App
async def receive_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        try:
            data = update.message.text
            user_data = json.loads(data)
            user_id = user_data.get("user_id")
            balance = user_data.get("balance")
            # Сохрани данные пользователя в базе данных (реализуй по необходимости)
            await update.message.reply_text("Данные успешно получены и сохранены!")
        except Exception as e:
            logger.error(f"Ошибка при получении данных из Web App: {e}")
            await update.message.reply_text("Произошла ошибка при обработке данных.")

# Команда /products для отображения списка продуктов
async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    row = []
    for idx, product in enumerate(PRODUCTS):
        button = InlineKeyboardButton(product["name"], callback_data=f"product_{idx}")
        row.append(button)
        if (idx + 1) % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери продукт:", reply_markup=reply_markup)

# Обработчик нажатий на кнопки продуктов
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("product_"):
        product_idx = int(data.split("_")[1])
        product = PRODUCTS[product_idx]
        keyboard = []
        for variation in product["variations"]:
            button = InlineKeyboardButton(
                f"Купить {variation['name']} за {variation['price']}",
                callback_data=f"buy_{product_idx}_{variation['name']}"
            )
            keyboard.append([button])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Выбран продукт: **{product['name']}**\nВыберите вариацию для покупки:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    elif data.startswith("buy_"):
        parts = data.split("_")
        product_idx = int(parts[1])
        variation_name = "_".join(parts[2:])
        product = PRODUCTS[product_idx]
        variation = next((v for v in product["variations"] if v["name"] == variation_name), None)
        if variation:
            # Реализуй процесс покупки (оплата, обновление баланса и т.д.)
            await query.edit_message_text(
                text=f"Вы успешно приобрели **{variation['name']}** за **{variation['price']}**!",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text("Произошла ошибка при покупке.")

# Обработка ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Основная функция для запуска бота
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("products", show_products))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_webapp_data))

    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
