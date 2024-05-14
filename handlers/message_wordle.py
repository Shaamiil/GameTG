from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from function_wordle import get_word, load_words_from_file
from keyboards import reply_wordle, reply


messageWordle_router = Router()
russian_word = load_words_from_file("russian.txt")


@messageWordle_router.message(F.text == "Назад", StateFilter)
async def account(message: types.Message, state: FSMContext):
    await message.answer("Будете играть?", reply_markup=reply.play)
    await state.clear()


@messageWordle_router.message(F.text == "Играть")
async def play(message: types.Message):
    if message.from_user.id == 579218344:
        await message.answer(text=f'Привет гомосек\n'
                                  f'Во что будешь играть',
                             reply_markup=reply.game_selection
                             )
    elif message.from_user.id == 596438415:
        await message.answer(text=f'Привет принцесса\n'
                                  f'Во что будешь играть',
                             reply_markup=reply.game_selection
                             )
    else:
        await message.answer(text="Выберите игру", reply_markup=reply.game_selection)


@messageWordle_router.message(F.text == "🌏Wordle")
async def rule_world(message: types.Message):
    await message.answer(text="Хотите ознакомиться с правилами игры?", reply_markup=reply_wordle.ready_wordle)


@messageWordle_router.message(F.text == "📘 Правила")
async def rules(message: types.Message):
    await message.answer(
        text=f'1️⃣ Задача игры отгадать спрятанное слово, состоит оно всегда из 5 букв\n\n'
             f'2️⃣ После нажатия кнопки "Начать" можете написать любое слово из 5 букв, после этого обратите внимание на ваше слово\n\n'
             f'3️⃣ Если буквы никак не изменились значит в скрытом слове таких букв нет. Если какие то буквы стали подчеркнутыми, то такие буквы есть в скрытом слове, но находятся в другой ячейке. Если буквы стали заглавными, значит буквы находятся на своем месте.\n\n'
             f'4️⃣ Обратите внимание, что буквы в слове могут повторяться, то есть если буква подчеркнута или стала заглавной, она может встречаться в слове как один раз, так и более одного раза.\n\n'
             f'5️⃣ Далее введите следующее слово. При этом учитывайте информацию о буквах и их расположении, полученную в предыдущем раунде\n\n'
             f'6️⃣ Продолжайте вводить слова, пока не угадаете спрятанное слово.  ️❗️ Но учтите если не угадаете слово за 5 раундов вы проиграете.',
        reply_markup=reply_wordle.ready_p_wordle
    )


@messageWordle_router.message(F.text == "Начать!")
async def start_game(message: types.Message, state: FSMContext):
    await message.answer(
        text=f'Введите первое слово из 5 букв'
    )
    await state.set_state("OneWord")


@messageWordle_router.message(StateFilter("OneWord"), F.text)
async def get_one_letter(message: types.Message, state: FSMContext):
    word = await get_word()
    s = 0
    marked_word = ""
    user_word1 = message.text.lower()
    if user_word1 == word:
        await state.clear()
        return await message.answer(
            text="Поздравляю, вы угадали слово с 1 раза",
            reply_markup=reply.game_selection
        )
    if not user_word1.isalpha():
        return await message.answer(text="Не нужно вводить лишние символы 👺")
    if len(user_word1) > 5 or len(user_word1) < 5:
        return await message.answer(text="Введите слово из 5 букв 😡")
    if user_word1 not in russian_word:
        return await message.answer(text="Такого слова не существует")
    else:
        for i in user_word1:
            if i in word:
                s += 1
        if s == 0:
            await state.update_data({"word": word})
            await state.update_data({"user_word1": user_word1})
            await state.set_state("TwoWord")
            await message.answer(
                text=f'В слове {user_word1} не найдено совпадений'
            )
            await state.update_data({"marked_word": user_word1})
            return await message.answer(
                text=f"Введите второе слово"
            )
        else:
            for i in range(len(word)):
                if user_word1[i] == word[i]:
                    marked_word += user_word1[i].upper()  # Помечаем букву заглавной
                elif user_word1[i] in word:
                    marked_word += f"<u>{user_word1[i]}</u>"  # Подчеркиваем букву
                else:
                    marked_word += user_word1[i]  # Оставляем букву без изменений
                await state.update_data({"marked_word": marked_word})
    await message.answer(marked_word, parse_mode='HTML')
    await message.answer(text="Введите второе слово")
    await state.update_data({"word": word})
    await state.set_state("TwoWord")


@messageWordle_router.message(StateFilter("TwoWord"), F.text)
async def get_one_letter(message: types.Message, state: FSMContext):
    data = await state.get_data()
    marked_word = data.get("marked_word")
    word = data.get("word")
    s = 0
    marked_word2 = ""
    user_word2 = message.text.lower()
    if user_word2 == word:
        await state.clear()
        return await message.answer(
            text="Поздравляю, вы угадали слово со 2 раза",
            reply_markup=reply.game_selection
        )
    if not user_word2.isalpha():
        return await message.answer(text="Не нужно вводить лишние символы 👺")
    if len(user_word2) > 5 or len(user_word2) < 5:
        return await message.answer(text="Введите слово из 5 букв 😡")
    if user_word2 not in russian_word:
        return await message.answer(text="Такого слова не существует")
    else:
        for i in user_word2:
            if i in word:
                s += 1
        if s == 0:
            await state.update_data({"word": word})
            await state.update_data({"user_word2": user_word2})
            await state.set_state("ThreeWord")
            await message.answer(
                text=f'{marked_word}\n'
                     f'В слове {user_word2} не найдено совпадений',
                parse_mode='HTML'
            )
            await state.update_data({"marked_word2": user_word2})
            return await message.answer(
                text=f"Введите третье слово"
            )
        else:
            for i in range(len(word)):
                if user_word2[i] == word[i]:
                    marked_word2 += user_word2[i].upper()  # Помечаем букву заглавной
                elif user_word2[i] in word:
                    marked_word2 += f"<u>{user_word2[i]}</u>"
                else:
                    marked_word2 += user_word2[i]  # Оставляем букву без изменений
                await state.update_data({"marked_word2": marked_word2})
    await message.answer(
        text=f'{marked_word}\n'
             f'{marked_word2}',
        parse_mode='HTML'
    )
    await message.answer(text="Введите третье слово")
    await state.set_state("ThreeWord")


@messageWordle_router.message(StateFilter("ThreeWord"), F.text)
async def get_one_letter(message: types.Message, state: FSMContext):
    data = await state.get_data()
    marked_word = data.get("marked_word")
    marked_word2 = data.get("marked_word2")
    word = data.get("word")
    s = 0
    marked_word3 = ""
    user_word3 = message.text.lower()
    if user_word3 == word:
        await state.clear()
        return await message.answer(
            text="Поздравляю, вы угадали слово с 3 раза",
            reply_markup=reply.game_selection
        )
    if not user_word3.isalpha():
        return await message.answer(text="Не нужно вводить лишние символы 👺")
    if len(user_word3) > 5 or len(user_word3) < 5:
        return await message.answer(text="Введите слово из 5 букв 😡")
    if user_word3 not in russian_word:
        return await message.answer(text="Такого слова не существует")
    else:
        for i in user_word3:
            if i in word:
                s += 1
        if s == 0:
            await state.update_data({"word": word})
            await state.update_data({"user_word3": user_word3})
            await state.set_state("FourWord")
            await message.answer(
                text=f'{marked_word}\n'
                     f'{marked_word2}\n'
                     f'В слове {user_word3} не найдено совпадений',
                parse_mode='HTML'
            )
            await state.update_data({"marked_word3": user_word3})
            return await message.answer(
                text=f"Введите четвертое слово"
            )
        else:
            for i in range(len(word)):
                if user_word3[i] == word[i]:
                    marked_word3 += user_word3[i].upper()  # Помечаем букву заглавной
                elif user_word3[i] in word:
                    marked_word3 += f"<u>{user_word3[i]}</u>"
                else:
                    marked_word3 += user_word3[i]  # Оставляем букву без изменений
                await state.update_data({"marked_word3": marked_word3})
    await message.answer(
        text=f'{marked_word}\n'
             f'{marked_word2}\n'
             f'{marked_word3}',
        parse_mode='HTML'
    )
    await state.update_data({"word": word})
    await message.answer(text="Введите четвертое слово")
    await state.set_state("FourWord")


@messageWordle_router.message(StateFilter("FourWord"), F.text)
async def get_one_letter(message: types.Message, state: FSMContext):
    data = await state.get_data()
    marked_word = data.get("marked_word")
    marked_word2 = data.get("marked_word2")
    marked_word3 = data.get("marked_word3")
    word = data.get("word")
    s = 0
    global marked_word4
    marked_word4 = ""
    user_word4 = message.text.lower()
    if user_word4 == word:
        await state.clear()
        return await message.answer(
            text="Поздравляю, вы угадали слово с 4 раза",
            reply_markup=reply.game_selection
        )
    if not user_word4.isalpha():
        return await message.answer(text="Не нужно вводить лишние символы 👺")
    if len(user_word4) > 5 or len(user_word4) < 5:
        return await message.answer(text="Введите слово из 5 букв 😡")
    if user_word4 not in russian_word:
        return await message.answer(text="Такого слова не существует")
    else:
        for i in user_word4:
            if i in word:
                s += 1
        if s == 0:
            await state.update_data({"word": word})
            await state.update_data({"user_word4": user_word4})
            await state.set_state("FourWord")
            await message.answer(
                text=f'{marked_word}\n'
                     f'{marked_word2}\n'
                     f'{marked_word3}\n'
                     f'В слове {user_word4} не найдено совпадений',
                parse_mode='HTML'
            )
            await state.update_data({"marked_word4": user_word4})
            return await message.answer(
                text=f"Введите пятое слово"
            )
        else:
            for i in range(len(word)):
                if user_word4[i] == word[i]:
                    marked_word4 += user_word4[i].upper()  # Помечаем букву заглавной
                elif user_word4[i] in word:
                    marked_word4 += f"<u>{user_word4[i]}</u>"
                else:
                    marked_word4 += user_word4[i]  # Оставляем букву без изменений
                await state.update_data({"marked_word4": marked_word4})
    await message.answer(
        text=f'{marked_word}\n{marked_word2}\n{marked_word3}\n{marked_word4}',
        parse_mode='HTML'
    )
    await message.answer(text="Введите пятое слово")
    await state.set_state("FiveWord")


@messageWordle_router.message(StateFilter("FiveWord"), F.text)
async def get_one_letter(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    user_word5 = message.text.lower()
    if not user_word5.isalpha():
        return await message.answer(text="Не нужно вводить лишние символы 👺")
    if len(user_word5) > 5 or len(user_word5) < 5:
        return await message.answer(text="Введите слово из 5 букв 😡")
    if user_word5 not in russian_word:
        return await message.answer(text="Такого слова не существует")
    if user_word5 == word:
        await state.clear()
        return await message.answer(
            text="Поздравляю, вы угадали слово с 5 раза🤨",
            reply_markup=reply.game_selection
        )
    else:
        await state.clear()
        return await message.answer(
            text=f'Хахай, вы проиграли 😂\n'
                 f'Правильное слово было "{word}"',
            reply_markup=reply.game_selection
        )
    # if not user_word5.isalpha():
    #     return await message.answer(text="Не нужно вводить лишние символы 👺")
    # if len(user_word5) > 5 or len(user_word5) < 5:
    #     return await message.answer(text="Введите слово из 5 букв 😡")
    # else:
    #     for i in user_word5:
    #         if i in word:
    #             s += 1
    #     if s == 0:
    #         await state.set_state("FiveWord")
    #         await message.answer(
    #             text=f'{marked_word}\n'
    #                  f'{marked_word2}\n'
    #                  f'{marked_word3}\n'
    #                  f'{marked_word4}\n'
    #                  f'В слове {user_word5} не найдено совпадений'
    #         )
    #         return await message.answer(
    #             text=f"Вы проиграли 😂",
    #             reply_markup=reply.game_selection
    #         )
    #     else:
    #         for i in range(len(word)):
    #             if user_word5[i] == word[i]:
    #                 marked_word5 += user_word5[i].upper()  # Помечаем букву заглавной
    #             elif user_word5[i] in word:
    #                 marked_word5 += f"<u>{user_word5[i]}</u>"
    #             else:
    #                 marked_word5 += user_word5[i]  # Оставляем букву без изменений
    # await message.answer(
    #     text=f'{marked_word}\n{marked_word2}\n{marked_word3}\n{marked_word4}\n{marked_word5}',
    #     parse_mode='HTML'
    # )
