from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

ready_wordle = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📘 Правила"),
            KeyboardButton(text="Начать!")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

ready_p_wordle = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Начать!")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

