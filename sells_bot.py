import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import CommandStart
from configg import Token

bot = Bot(token=Token)
dp = Dispatcher()


products = {
    "olma": {
        "name": "Olma 🍎",
        "price": "10,000 so'm / kg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg",
    },
    "banan": {
        "name": "Banan 🍌",
        "price": "18,000 so'm / kg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg",
    },
    "anor": {
        "name": "Anor ❤️",
        "price": "25,000 so'm / kg",
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Pomegranate_fruit_-_whole_and_split.jpg",
    },
    "uzum": {
        "name": "Uzum 🍇",
        "price": "9,000 so'm / kg",
        "image": "https://clck.ru/3NodqC",
    },
    "kiwi": {
        "name": "Kiwi 🥝",
        "price": "37,990 so‘m / 1 kg",
        "image": "clck.ru/3Noe7m",
    },
    "Apelsin": {
        "name": "Apelsin 🍊",
        "price": "47,490 so‘m / 1 kg",
        "image": "clck.ru/3NoeEv",
    },
    "Mandarin": {
        "name": "Mandarin 🍊",
        "price": "9,257.81 so‘m/kg ",
        "image": "clck.ru/3NoePH",
    },
    "Gilos": {
        "name": "Gilos 🍒",
        "price": "17,000 so‘m/kg ",
        "image": "clck.ru/3Noefa",
    },
    "O'rik": {
        "name": "O‘rik 🍑",
        "price": "5,000 so‘m/kg ",
        "image": "clck.ru/3Noeqn",
    },
    "Nok": {
        "name": "Nok 🍐",
        "price": "5,000 so‘m/kg ",
        "image": "clck.ru/3Noeqn",
    },
    "Ananas": {
        "name": "Ananas 🍍",
        "price": "15,000 so‘m/kg",
        "image": "clck.ru/3Nof6e",
    },
}


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=product["name"], callback_data=key)]
        for key, product in products.items()
    ]
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(" Qaysi mahsulotni sotib olmoqchisiz?", reply_markup=main_menu)


@dp.callback_query(F.data.in_(products.keys()))
async def product_detail(callback: CallbackQuery):
    product_key = callback.data
    product = products[product_key]

    text = f" Mahsulot: {product['name']}\n Narxi: {product['price']}"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Sotib olish", callback_data=f"buy_{product_key}"
                )
            ],
            [InlineKeyboardButton(text=" Orqaga", callback_data="back")],
        ]
    )

    await callback.message.delete()
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo=product["image"],
        caption=text,
        reply_markup=keyboard,
    )


@dp.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: CallbackQuery):
    product_key = callback.data.replace("buy_", "")
    product = products[product_key]

    await callback.answer()
    await callback.message.answer(
        f"✅ Siz {product['name']} ni {product['price']} ga sotib oldingiz. Tez orada siz bilan bog'lanamiz!"
    )


@dp.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        " Qaysi mahsulotni sotib olmoqchisiz?", reply_markup=main_menu
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
