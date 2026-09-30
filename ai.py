import os

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# =========================
# КАТАЛОГ
# =========================

PRODUCTS = {
    "🦴 Канат «Грызун»": {
        "price": 790,
        "description": "Прочный хлопковый канат для жевания и перетягивания.",
        "material": "Хлопок",
        "suitable": "Средние и крупные собаки",
    },

    "🥎 Мяч «Бум»": {
        "price": 590,
        "description": "Прочный мяч для апортировки и активных игр.",
        "material": "Прочный полимер",
        "suitable": "Собаки разных размеров",
    },

    "🧸 Лисёнок-пищалка": {
        "price": 890,
        "description": "Мягкая игрушка с пищалкой.",
        "material": "Текстиль",
        "suitable": "Маленькие и средние собаки",
    },

    "⭕ Кольцо «Зубастик»": {
        "price": 690,
        "description": "Резиновое кольцо для жевания и активных игр.",
        "material": "Резина",
        "suitable": "Средние и крупные собаки",
    },

    "🧩 Головоломка «Умник»": {
        "price": 1290,
        "description": "Развивающая игрушка для лакомств.",
        "material": "Пищевой пластик",
        "suitable": "Собаки разных размеров",
    },
}


# =========================
# МЕНЮ
# =========================

def main_menu():
    keyboard = [
        ["🛒 Покупка"],
        ["📦 Каталог"],
        ["❓ Вопрос по товару"],
        ["↩️ Возврат"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def product_menu():
    keyboard = []

    for product_name in PRODUCTS:
        keyboard.append([product_name])

    keyboard.append(["🏠 Главное меню"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def question_menu():
    keyboard = [
        ["💰 Цена"],
        ["🧱 Материал"],
        ["🐕 Подходит ли моей собаке?"],
        ["📝 Описание"],
        ["🏠 Главное меню"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def return_menu():
    keyboard = [
        ["📋 Условия возврата"],
        ["↩️ Оформить возврат"],
        ["🏠 Главное меню"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# =========================
# /start
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()

    await update.message.reply_text(
        "🐶 Добро пожаловать в магазин «Лапка»!\n\n"
        "Я помогу выбрать игрушку для вашей собаки.\n\n"
        "Выберите нужный раздел:",
        reply_markup=main_menu()
    )


# =========================
# КАТАЛОГ
# =========================

async def show_catalog(update: Update):
    text = "📦 Наши игрушки:\n\n"

    for name, product in PRODUCTS.items():
        text += (
            f"{name}\n"
            f"💰 {product['price']} ₽\n"
            f"🐕 {product['suitable']}\n\n"
        )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


# =========================
# ВЫБОР ТОВАРА ДЛЯ ПОКУПКИ
# =========================

async def show_buy_products(update: Update):
    context = update.get_bot().get_chat

    await update.message.reply_text(
        "🛒 Выберите игрушку:",
        reply_markup=product_menu()
    )


# =========================
# КАРТОЧКА ТОВАРА
# =========================

async def show_product(update: Update, product_name: str):
    product = PRODUCTS[product_name]

    keyboard = [
        ["✅ Купить"],
        ["⬅️ Выбрать другую игрушку"],
        ["🏠 Главное меню"],
    ]

    await update.message.reply_text(
        f"{product_name}\n\n"
        f"💰 Цена: {product['price']} ₽\n"
        f"📝 {product['description']}\n"
        f"🧱 Материал: {product['material']}\n"
        f"🐕 Подходит: {product['suitable']}\n\n"
        f"Хотите оформить заказ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )


# =========================
# ВОПРОСЫ ПО ТОВАРУ
# =========================

async def show_question_products(update: Update):
    await update.message.reply_text(
        "❓ Выберите товар:",
        reply_markup=product_menu()
    )


async def show_questions(
    update: Update,
    product_name: str
):
    await update.message.reply_text(
        f"❓ Что хотите узнать о товаре:\n"
        f"{product_name}",
        reply_markup=question_menu()
    )


async def answer_question(
    update: Update,
    question: str,
    product_name: str
):
    product = PRODUCTS[product_name]

    if question == "💰 Цена":
        answer = (
            f"💰 Цена «{product_name}» — "
            f"{product['price']} ₽."
        )

    elif question == "🧱 Материал":
        answer = (
            f"🧱 Материал игрушки — "
            f"{product['material']}."
        )

    elif question == "🐕 Подходит ли моей собаке?":
        answer = (
            f"🐕 Игрушка подходит для: "
            f"{product['suitable']}."
        )

    elif question == "📝 Описание":
        answer = (
            f"📝 {product['description']}"
        )

    else:
        answer = "Информация не найдена."

    await update.message.reply_text(
        answer,
        reply_markup=question_menu()
    )


# =========================
# ВОЗВРАТ
# =========================

async def show_return(update: Update):
    await update.message.reply_text(
        "↩️ Раздел возврата.\n\n"
        "Выберите действие:",
        reply_markup=return_menu()
    )


async def return_rules(update: Update):
    await update.message.reply_text(
        "📋 Условия возврата:\n\n"
        "• товар можно вернуть в течение 14 дней;\n"
        "• товар должен сохранить товарный вид;\n"
        "• для оформления потребуется номер заказа.",
        reply_markup=return_menu()
    )


async def return_request(update: Update):
    await update.message.reply_text(
        "↩️ Заявка на возврат создана!\n\n"
        "Номер заявки: #RET-001\n"
        "Менеджер свяжется с вами.",
        reply_markup=main_menu()
    )


# =========================
# ГЛАВНЫЙ ОБРАБОТЧИК
# =========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    # Главное меню
    if text == "🏠 Главное меню":
        context.user_data.clear()

        await update.message.reply_text(
            "🐶 Главное меню:",
            reply_markup=main_menu()
        )
        return

    # Покупка
    if text == "🛒 Покупка":
        context.user_data["mode"] = "buy"

        await show_buy_products(update)
        return

    # Каталог
    if text == "📦 Каталог":
        await show_catalog(update)
        return

    # Вопрос по товару
    if text == "❓ Вопрос по товару":
        context.user_data["mode"] = "question"

        await show_question_products(update)
        return

    # Возврат
    if text == "↩️ Возврат":
        await show_return(update)
        return

    # Условия возврата
    if text == "📋 Условия возврата":
        await return_rules(update)
        return

    # Оформление возврата
    if text == "↩️ Оформить возврат":
        await return_request(update)
        return

    # Выбор товара
    if text in PRODUCTS:
        context.user_data["selected_product"] = text

        mode = context.user_data.get("mode")

        if mode == "buy":
            await show_product(update, text)

        elif mode == "question":
            await show_questions(update, text)

        return

    # Вопрос о товаре
    questions = [
        "💰 Цена",
        "🧱 Материал",
        "🐕 Подходит ли моей собаке?",
        "📝 Описание",
    ]

    if text in questions:
        product_name = context.user_data.get(
            "selected_product"
        )

        if product_name:
            await answer_question(
                update,
                text,
                product_name
            )

        return

    # Купить
    if text == "✅ Купить":
        product_name = context.user_data.get(
            "selected_product"
        )

        if product_name:
            product = PRODUCTS[product_name]

            await update.message.reply_text(
                "✅ Заказ оформлен!\n\n"
                f"🧸 {product_name}\n"
                f"💰 {product['price']} ₽\n\n"
                "📦 Номер заказа: #DOG-001\n"
                "Спасибо за покупку! 🐶",
                reply_markup=main_menu()
            )

        return

    # Другая игрушка
    if text == "⬅️ Выбрать другую игрушку":
        context.user_data["mode"] = "buy"

        await show_buy_products(update)
        return

    # Неизвестная команда
    await update.message.reply_text(
        "🐾 Пожалуйста, выберите действие "
        "с помощью кнопок.",
        reply_markup=main_menu()
    )


# =========================
# ЗАПУСК БОТА
# =========================

def main():
    if not TOKEN:
        raise ValueError(
            "Не найден TELEGRAM_BOT_TOKEN в файле .env"
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("🐶 Delka_01Bot запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()