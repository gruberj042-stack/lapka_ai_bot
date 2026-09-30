from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
from dotenv import load_dotenv

from intent_model import predict_intent, predict_product


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "images"
)


PRODUCTS = {
    "🦴 Канат «Грызун»": {
        "price": 790,
        "description": "Прочный хлопковый канат для жевания и перетягивания.",
        "suitable": "Средние и крупные собаки",
        "material": "Хлопок",
        "image": "rope.jpeg",
    },
    "🥎 Мяч «Бум»": {
        "price": 590,
        "description": "Прочный мяч для апортировки и активных игр.",
        "suitable": "Собаки разных размеров",
        "material": "Прочный полимер",
        "image": "ball.jpeg",
    },
    "🧸 Лисёнок-пищалка": {
        "price": 890,
        "description": "Мягкая игрушка с пищалкой.",
        "suitable": "Маленькие и средние собаки",
        "material": "Текстиль",
        "image": "fox.jpeg",
    },
    "⭕ Кольцо «Зубастик»": {
        "price": 690,
        "description": "Резиновое кольцо для жевания и активных игр.",
        "suitable": "Средние и крупные собаки",
        "material": "Резина",
        "image": "ring.jpeg",
    },
    "🧩 Головоломка «Умник»": {
        "price": 1290,
        "description": "Развивающая игрушка, куда можно спрятать лакомство.",
        "suitable": "Собаки разных размеров",
        "material": "Пищевой пластик",
        "image": "puzzle.jpeg",
    },
}


def main_menu():
    keyboard = [
        ["🛒 Купить игрушку"],
        ["📦 Каталог"],
        ["❓ Вопрос по товару"],
        ["↩️ Возврат"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def products_menu():
    keyboard = []

    for product in PRODUCTS:
        keyboard.append([product])

    keyboard.append(["⬅️ Главное меню"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def question_menu():
    keyboard = [
        ["💰 Цена"],
        ["🧱 Материал"],
        ["🐕 Для какой собаки?"],
        ["📝 Описание"],
        ["⬅️ Главное меню"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def return_menu():
    keyboard = [
        ["↩️ Хочу вернуть товар"],
        ["📋 Условия возврата"],
        ["⬅️ Главное меню"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def send_product_card(
    update: Update,
    product_name: str,
    reply_markup
):
    product = PRODUCTS[product_name]

    image_path = os.path.join(
        IMAGES_DIR,
        product["image"]
    )

    text = (
        f"{product_name}\n\n"
        f"💰 Цена: {product['price']} ₽\n"
        f"📝 {product['description']}\n"
        f"🐕 Подходит: {product['suitable']}\n"
        f"🧱 Материал: {product['material']}"
    )

    if os.path.exists(image_path):

        with open(image_path, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=text,
                reply_markup=reply_markup
            )

    else:

        await update.message.reply_text(
            "⚠️ Картинка товара пока не найдена.\n\n"
            + text,
            reply_markup=reply_markup
        )


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()

    await update.message.reply_text(
        "🐶 Добро пожаловать в магазин «Лапка»!\n\n"
        "Я помогу выбрать игрушку для вашей собаки, "
        "ответить на вопросы и оформить возврат.\n\n"
        "Выберите действие или напишите свой вопрос:",
        reply_markup=main_menu()
    )


async def show_catalog(update: Update):

    text = "📦 Наш каталог игрушек:\n\n"

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


async def show_buy_menu(update: Update):

    await update.message.reply_text(
        "🛒 Выберите игрушку:",
        reply_markup=products_menu()
    )


async def show_product_for_buy(
    update: Update,
    product_name: str
):

    keyboard = [
        ["✅ Купить"],
        ["⬅️ К выбору игрушек"],
        ["⬅️ Главное меню"],
    ]

    await send_product_card(
        update,
        product_name,
        ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )


async def show_question_products(update: Update):

    await update.message.reply_text(
        "❓ Выберите товар:",
        reply_markup=products_menu()
    )


async def show_questions(
    update: Update,
    product_name: str
):

    await send_product_card(
        update,
        product_name,
        question_menu()
    )


async def answer_question(
    update: Update,
    question: str,
    product_name: str
):

    product = PRODUCTS[product_name]

    if question == "💰 Цена":

        answer = f"💰 Цена товара — {product['price']} ₽."

    elif question == "🧱 Материал":

        answer = f"🧱 Материал: {product['material']}."

    elif question == "🐕 Для какой собаки?":

        answer = (
            f"🐕 Игрушка подходит для: "
            f"{product['suitable']}."
        )

    elif question == "📝 Описание":

        answer = f"📝 {product['description']}"

    else:

        answer = "Не удалось найти информацию."

    await update.message.reply_text(
        answer,
        reply_markup=question_menu()
    )


async def show_return_menu(update: Update):

    await update.message.reply_text(
        "↩️ Раздел возврата.\n\n"
        "Выберите нужный вариант:",
        reply_markup=return_menu()
    )


async def return_info(update: Update):

    await update.message.reply_text(
        "📋 Условия возврата:\n\n"
        "• товар можно вернуть в течение 14 дней;\n"
        "• игрушка должна сохранить товарный вид;\n"
        "• необходимо указать номер заказа.\n\n"
        "Если хотите оформить возврат, нажмите "
        "«↩️ Хочу вернуть товар».",
        reply_markup=return_menu()
    )


async def start_return(update: Update):

    await update.message.reply_text(
        "↩️ Хорошо!\n\n"
        "Для оформления возврата нажмите:\n"
        "📩 Оформить заявку\n\n"
        "После этого нужно будет указать номер заказа.",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["📩 Оформить заявку"],
                ["⬅️ Главное меню"],
            ],
            resize_keyboard=True
        )
    )


# =========================
# ИИ
# =========================

async def handle_ai_intent(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    intent = predict_intent(text)
    product = predict_product(text)

    # Если это вопрос по товару
    # и товар удалось определить

    if intent == "Вопрос по товару" and product:

        context.user_data["mode"] = "question"
        context.user_data["selected_product"] = product

        await send_product_card(
            update,
            product,
            question_menu()
        )

        return True

    # Покупка

    if intent == "Покупка":

        context.user_data["mode"] = "buy"

        await update.message.reply_text(
            "🛒 Похоже, вы хотите купить игрушку!\n\n"
            "Выберите товар:",
            reply_markup=products_menu()
        )

        return True

    # Возврат

    if intent == "Возврат":

        context.user_data["mode"] = "return"

        await update.message.reply_text(
            "↩️ Похоже, вы хотите оформить возврат.\n\n"
            "Выберите нужный вариант:",
            reply_markup=return_menu()
        )

        return True

    # Вопрос по товару,
    # но товар не определён

    if intent == "Вопрос по товару":

        context.user_data["mode"] = "question"

        await update.message.reply_text(
            "❓ Вы хотите узнать информацию о товаре.\n\n"
            "Выберите товар:",
            reply_markup=products_menu()
        )

        return True

    return False


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if text == "🛒 Купить игрушку":

        context.user_data["mode"] = "buy"

        await show_buy_menu(update)
        return

    if text == "📦 Каталог":

        await show_catalog(update)
        return

    if text == "❓ Вопрос по товару":

        context.user_data["mode"] = "question"

        await show_question_products(update)
        return

    if text == "↩️ Возврат":

        context.user_data["mode"] = "return"

        await show_return_menu(update)
        return

    if text == "⬅️ Главное меню":

        context.user_data.clear()

        await update.message.reply_text(
            "🐶 Главное меню:",
            reply_markup=main_menu()
        )
        return

    if text == "📋 Условия возврата":

        await return_info(update)
        return

    if text == "↩️ Хочу вернуть товар":

        await start_return(update)
        return

    if text == "📩 Оформить заявку":

        await update.message.reply_text(
            "✅ Заявка на возврат создана!\n\n"
            "Номер заявки: #RET-001\n"
            "Менеджер магазина свяжется с вами.",
            reply_markup=main_menu()
        )
        return

    if text in PRODUCTS:

        context.user_data["selected_product"] = text

        if context.user_data.get("mode") == "buy":

            await show_product_for_buy(
                update,
                text
            )

        elif context.user_data.get("mode") == "question":

            await show_questions(
                update,
                text
            )

        return

    if text in [
        "💰 Цена",
        "🧱 Материал",
        "🐕 Для какой собаки?",
        "📝 Описание",
    ]:

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

    if text == "✅ Купить":

        product_name = context.user_data.get(
            "selected_product"
        )

        product = PRODUCTS.get(product_name)

        if product:

            await update.message.reply_text(
                f"✅ Отличный выбор!\n\n"
                f"Товар: {product_name}\n"
                f"Цена: {product['price']} ₽\n\n"
                f"🛒 Заказ оформлен!\n"
                f"Номер заказа: #DOG-001",
                reply_markup=main_menu()
            )

        return

    if text == "⬅️ К выбору игрушек":

        context.user_data["mode"] = "buy"

        await show_buy_menu(update)
        return

    # =========================
    # ИИ
    # =========================

    ai_used = await handle_ai_intent(
        update,
        context
    )

    if ai_used:
        return

    await update.message.reply_text(
        "🐾 Я пока не совсем понял ваш запрос.\n\n"
        "Попробуйте написать, например:\n"
        "• «Хочу купить игрушку»\n"
        "• «Хочу вернуть товар»\n"
        "• «Из чего сделан мяч?»",
        reply_markup=main_menu()
    )


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