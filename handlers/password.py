from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from function_password import special_symbols, months, roman_numerals, str_digits, russian_letter, russian_letter_upper, \
    english_letter_upper, english_letter, wordle_day, elements, dict_country_random, dict_country
from keyboards import reply

password_router = Router()


@password_router.message(F.text == "🔒 Password")
async def password_handle(message: types.Message, state: FSMContext):
    await message.answer("Придумайте пароль")
    await state.set_state("password")


@password_router.message(StateFilter("password"))
async def password(message: types.Message, state: FSMContext):
    wordle = await wordle_day()
    country = dict_country_random()
    if " " in message.text:
        return await message.answer("В вашем пароле не должно быть пробелов")
    list_letter = []
    for letter in message.text:
        if letter in russian_letter or letter in russian_letter_upper or letter in english_letter_upper \
                or letter in english_letter:
            if letter.lower() not in list_letter:
                list_letter.append(letter.lower())
            else:
                return await message.answer(text="В вашем пароле не должно быть одинаковых букв")
    include_russian = False
    include_english = False
    for letter in russian_letter:
        if letter in message.text:
            include_russian = True
            break
    for letter in english_letter:
        if letter in message.text:
            include_english = True
            break
    if not (include_russian or include_english):
        return await message.answer(text="Пароль должен содеражть буквы")
    if len(message.text) < 10:
        return await message.answer("Пароль не должен быть короче 10 символов")
    include_digits = False
    for digit in str_digits:
        if digit in message.text:
            include_digits = True
            break
    if not include_digits:
        return await message.answer("Пароль должен содержать цифры")
    include_upper = False
    for letter in russian_letter_upper + english_letter_upper:
        if letter in message.text:
            include_upper = True
            break
    if not include_upper:
        return await message.answer("Пароль должен содержать заглавные буквы")
    include_symbols = False
    for symbols in special_symbols:
        if symbols in message.text:
            include_symbols = True
            break
    if not include_symbols:
        return await message.answer("Пароль должен содержать спецсимволы")
    listt = []
    for number in message.text:
        if number in str_digits:
            listt.append(int(number))
    if sum(listt) <= 25:
        return await message.answer("Сумма всех цифр в пароле должна быть больше 25")
    if sum(listt) % 3 != 0:
        return await message.answer("Сумма всех цифр должна быть кратна 3")
    # if str(sum(listt)*sum(listt)) not in message.text:
    #     return await message.answer(text="В вашем пароле должен быть квадрат суммы всех ваших чисел")
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
    if "LXV" not in message.text:
        return await message.answer("Ваша римская цифра должна быть равна 65")
    if "qGphJD" not in message.text and "DJhpGq" not in message.text:
        await message.answer_photo(
            photo="https://avatars.mds.yandex.net/i?id=27a8438251a808e94c9b7c3b76df165cf3daaff0-12497202-images-thumbs&n=13")
        return await message.answer("Ваш пароль должен содержать эту каптчу(на английском)")
    include_elements = False
    for element in elements:
        if element in message.text:
            include_elements = True
            break
    if not include_elements:
        return await message.answer("Ваш пароль должен включать любой двухбуквенный символ из таблицы Менделлева")
    await message.answer(
        "Ваш пароль должен включать слово дня из игры <a href='https://www.nytimes.com/games/wordle/index.html'>"
        "Wordle</a>", )
    await state.update_data({"wordle": wordle,
                             "country": country})
    await state.set_state("wordle")


@password_router.message(StateFilter("wordle"))
async def day_wordle(message: types.Message, state: FSMContext):
    data = await state.get_data()
    wordle = data.get("wordle")
    country = data.get("country")
    if wordle not in message.text:
        return await message.answer("Вы ввели не то слово")
    await message.answer("Ваш пароль должен включать название страны с картинки")
    await message.answer_photo(
        photo=country)
    await state.update_data({"password": message.text})
    await state.set_state("country")


@password_router.message(StateFilter("country"))
async def img_country(message: types.Message, state: FSMContext):
    data = await state.get_data()
    country = data.get("country")
    passwordd = data.get("password")
    if dict_country[country] not in message.text:
        return await message.answer("Неправильно(")
    await message.answer("Теперь введи свой пароль наоборот")
    await state.update_data({"password": message.text})
    await state.set_state("reverse")


@password_router.message(StateFilter("reverse"))
async def reverse_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    passwordd = data.get("password")
    new_password = passwordd[::-1]
    if message.text != new_password:
        return await message.answer("Неправильно! Введите свой пароль наоборот")
    await message.answer(text="Молодец, ты придумал(а) пароль", reply_markup=reply.play)
