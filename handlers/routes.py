
"""

Создать кнопки и сделать заглушки сегодня
Так же чуть разобраться как устоен SQLite

"""





from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Про бота")],
        [KeyboardButton(text="Старт"), KeyboardButton(text="Допомога")]
    ],
    resize_keyboard=True
)



@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def start(message: Message):
    await message.answer(
        "Привіт! Я персональний бот для вивчення мов.\n\n"
        "Напишіть /help для допомоги.",
        reply_markup=MAIN_KEYBOARD
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команди:\n"
        "<b>/start</b> - запуск бота\n"
        "<b>/help</b> - список команд\n"
        "<b>/about</b> - про нас",
        parse_mode="HTML",
        reply_markup=MAIN_KEYBOARD
    )


@router.message(F.text == "Допомога")
async def help_button(message: Message):
    await message.answer(
        "Розділ допомоги поки що в розробці.",
        reply_markup=MAIN_KEYBOARD
    )


@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer(
        "Інформація про бота буде додана пізніше.",
        reply_markup=MAIN_KEYBOARD
    )


@router.message(F.text == "Про бота")
async def about_button(message: Message):
    await message.answer(
        "Це бот для вивчення мов. Функціонал поступово додається.",
        reply_markup=MAIN_KEYBOARD
    )


@router.message()
async def clear_message(message: Message):
    await message.answer(
        "Такої команди немає!",
        reply_markup=MAIN_KEYBOARD
    )