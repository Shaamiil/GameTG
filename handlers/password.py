from aiogram import Router, F, types
from aiogram.client import bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from function_password import special_symbols, months, roman_numerals, str_digits, russian_letter, russian_letter_upper
from keyboards import reply

password_router = Router()


@password_router.message(F.text == "🔒 Password")
async def password_handle(message: types.Message, state: FSMContext):
    await message.answer("Придумайте пароль")
    await state.set_state("password")


@password_router.message(StateFilter("password"))
async def password(message: types.Message):
    include_letter = False
    for letter in russian_letter:
        if letter in message.text:
            include_letter = True
            break
    if not include_letter:
        return await message.answer(text="Пароль должен содеражть буквы")
    if len(message.text) < 5:
        return await message.answer("Пароль не должен быть короче 5 символов")
    include_digits = False
    for digit in str_digits:
        if digit in message.text:
            include_digits = True
            break
    if not include_digits:
        return await message.answer("Пароль должен содержать цифры")
    include_letter_upper = False
    for letter in russian_letter_upper:
        if letter in message.text:
            include_letter_upper = True
            break
    if not include_letter_upper:
        return await message.answer("Пароль должен содержать заглавные буквы")
    include_symbols = False
    for symbols in special_symbols:
        if symbols in message.text:
            include_symbols = True
            break
    if not include_symbols:
        return await message.answer("Пароль должен содержать спецсимволы")
    for i in message.text:
        listt = []
        if i in str_digits:
            listt.append(int(i))
            if sum(listt) != 25:
                return await message.answer("Сумма всех цифр в пароле должна быть 25")
    include_month = False
    for month in months:
        if month in message.text:
            include_month = True
            break
    if not include_month:
        return await message.answer("Ваш пароль должен включать месяц года")
    include_roman_numerals = False
    for numerals in roman_numerals:
        if numerals in message.text:
            include_roman_numerals = True
            break
    if not include_roman_numerals:
        return await message.answer("Ваш пароль должен включать хотя бы одну римскую цифру")
    if "XXXV" not in message.text:
        return await message.answer("Ваша римская цифра должна быть равна 35")
    if "ee610c" not in message.text:
        await message.answer_photo(
            photo="https://avatars.mds.yandex.net/i?id=b63075de51d98e8458544400b7815317_sr-5279278-images-thumbs&n=13")
        return await message.answer("Ваш пароль должен содержать эту каптчу")
    await message.answer(text="Молодец, ты придуамл пароль", reply_markup=reply.play)
