# import asyncio
# import os

# from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv


# load_dotenv()

# TOKEN = os.getenv("BOT_TOKEN")

# dp = Dispatcher()


# @dp.startup()
# async def on_startup():
#     print("Bot запущен!")


# async def main():
#     bot = Bot(token=TOKEN)

#     try:
#         await dp.start_polling(bot)
#     finally:
#         await bot.session.close()


# if __name__ == "__main__":
#     asyncio.run(main())





# import asyncio
# import os

# from aiogram import Bot, Dispatcher
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from dotenv import load_dotenv


# load_dotenv()

# TOKEN = os.getenv("BOT_TOKEN")

# dp = Dispatcher()


# @dp.message(CommandStart())
# async def command_start_handler(message: Message):
#     await message.answer(
#         "👋 Привет!\n\n"
#         "Я бот для работы с расписанием студентов. "
#     )


# async def main():
#     bot = Bot(token=TOKEN)

#     try:
#         await dp.start_polling(bot)
#     finally:
#         await bot.session.close()


# if __name__ == "__main__":
#     asyncio.run(main())





import asyncio
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
#新添加
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
#END
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

#添加代理
PROXY_URL = "http://127.0.0.1:7897"
session = AiohttpSession(proxy=PROXY_URL)
#END

dp = Dispatcher()


schedule = {
    "Понедельник": [
        ("11:30–13:00", "ВПД"),
        ("13:30–15:00", "ВПД"),
    ],
    "Вторник": [
        ("08:10–09:40", "Алгебра и алгоритмы"),
        ("09:50–11:20", "Математический анализ"),
        ("11:30–13:00", "Алгебра и алгоритмы"),
        ("13:30–15:00", "Математический анализ"),
        ("17:10–18:40", "Алгоритмы и структуры данных"),
    ],
    "Среда": [
        ("09:50–11:20", "Программирование"),
        ("11:30–13:00", "Программирование"),
        ("18:50–22:00", "Русский язык"),
    ],
    "Четверг": [
        ("15:30–17:00", "Введение в ОС Linux"),
    ],
    "Пятница": [
        ("08:10–09:40", "Дискретная математика"),
        ("09:50–11:20", "Дискретная математика"),
        ("15:30–17:00", "Возможность ИИ"),
    ],
    "Суббота": [
        ("13:30–15:00", "Русский язык (устная речь)"),
    ],
}


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📅 Сегодня"),
            KeyboardButton(text="📆 Завтра"),
        ],
        [
            KeyboardButton(text="🗓 На неделю"),
        ],
        [
            KeyboardButton(text="ℹ️ Помощь"),
        ],
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я бот для работы с расписанием студентов.\n\n"
        "Выберите действие:",
        reply_markup=keyboard
    )


@dp.message()
async def message_handler(message: Message):
    if message.text == "🗓 На неделю":
        text = "🗓 Расписание на неделю:\n\n"

        for day, lessons in schedule.items():
            text += f"📌 {day}\n"

            for time, subject in lessons:
                text += f"{time} — {subject}\n"

            text += "\n"

        await message.answer(text)

    elif message.text == "ℹ️ Помощь":
        await message.answer(
            "ℹ️ Помощь\n\n"
            "Используйте кнопки меню для просмотра расписания.\n\n"
            "Доступные функции:\n"
            "📅 расписание на сегодня\n"
            "📆 расписание на завтра\n"
            "🗓 расписание на неделю"
        )

    elif message.text == "📅 Сегодня":
        days = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье",
        }

        today = datetime.now()
        day_name = days[today.weekday()]

        if day_name in schedule:
            text = f"📅 Расписание на сегодня — {day_name}:\n\n"

            for time, subject in schedule[day_name]:
                text += f"{time} — {subject}\n"

            await message.answer(text)
        else:
            await message.answer(
                f"📅 Сегодня — {day_name}.\n\n"
                "Занятий по расписанию нет."
            )

    elif message.text == "📆 Завтра":
        days = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье",
        }

        tomorrow = datetime.now() + timedelta(days=1)
        day_name = days[tomorrow.weekday()]

        if day_name in schedule:
            text = f"📆 Расписание на завтра — {day_name}:\n\n"

            for time, subject in schedule[day_name]:
                text += f"{time} — {subject}\n"

            await message.answer(text)
        else:
            await message.answer(
                f"📆 Завтра — {day_name}.\n\n"
                "Занятий по расписанию нет."
            )

    else:
        await message.answer(
            "Пожалуйста, выберите действие с помощью кнопок меню."
        )


async def main():
    bot = Bot(token=TOKEN, session=session)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())