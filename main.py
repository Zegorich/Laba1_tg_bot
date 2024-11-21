from config import token
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile

dp = Dispatcher()  # Создаем экземпляр диспетчера, который будет обрабатывать входящие сообщения

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Картинка'), KeyboardButton(text='Аудио')]
], resize_keyboard=True)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n" 
        f"Код программы можно посмотреть отправив сообщение /gitrep",
        reply_markup=kb
    )

@dp.message(Command("gitrep"))
async def custom_command_code(message: Message) -> None:
    await message.answer(f"Код проекта представлен на платформе {html.bold('Github')}: https://github.com/Zegorich/Laba1_tg_bot")

@dp.message(F.text == "Картинка")
async def send_image_choice(message: Message) -> None:
    await message.answer(
        "Выберите цифру от 1 до 3, чтобы получить картинку:\n1. Лягушка\n2. Мышка\n3. Собачка"
    )

@dp.message(F.text == "Аудио")
async def send_audio(message: Message) -> None:
    audio = FSInputFile('audio/Sonne.mp3')
    await message.answer_audio(audio=audio)

@dp.message(F.text.in_(['1', '2', '3']))
async def send_selected_image(message: Message) -> None:
    image_choices = {
        '1': 'photo/frog.png',
        '2': 'photo/mouse.png',
        '3': 'photo/dog.png'
    }

    choice = message.text
    photo = FSInputFile(image_choices[choice])
    await message.answer_photo(photo=photo)

@dp.message(F.text.not_in(['1', '2', '3']))
async def invalid_choice(message: Message) -> None:
    await message.answer("Некорректный выбор, выберите цифру от 1 до 3.")

async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

# Настройка логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    asyncio.run(main())