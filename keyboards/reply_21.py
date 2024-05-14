from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

ready_21 = ReplyKeyboardMarkup(
    keyboard=[
        [
            # английские "а"
            KeyboardButton(text="📗 Правила"),
            KeyboardButton(text="Нaчaть!")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

ready_p_21 = ReplyKeyboardMarkup(
    keyboard=[
        [
            # английские "а"
            KeyboardButton(text="Нaчaть!")
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
            KeyboardButton(text="🤖 С ботом"),
            KeyboardButton(text="🫂 С Другом")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

choosing_an_action = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Взять карту"),
            KeyboardButton(text="Пропустить ход")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)