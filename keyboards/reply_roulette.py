from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

ready_roulette = ReplyKeyboardMarkup(
    keyboard=[
        [
            # английская "H"
            KeyboardButton(text="📕 Правила"),
            KeyboardButton(text="Hачать!")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)


ready_p_roulette = ReplyKeyboardMarkup(
    keyboard=[
        [
            # английская "H"
            KeyboardButton(text="Hачать!")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)


players = ReplyKeyboardMarkup(
    keyboard=[
        [
            # английские о
            KeyboardButton(text="🤖 С бoтoм"),
            KeyboardButton(text="🫂 С Другoм")
        ],
        [
            KeyboardButton(text="📕 Правила")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

shoot = ReplyKeyboardMarkup(
    keyboard=[
        [
            # английские о
            KeyboardButton(text="Выстрелить в себя"),
            KeyboardButton(text="Выстрелить в бота")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)