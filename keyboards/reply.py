from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
play = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Играть")
        ]
    ],
    resize_keyboard=True
)

game_selection = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌏Wordle"),
            KeyboardButton(text="🃏21")
        ],
        [
            KeyboardButton(text="🔒 Password"),
            KeyboardButton(text="🩸 Buckshot Roulette")
        ]
    ],
    resize_keyboard=True
)
