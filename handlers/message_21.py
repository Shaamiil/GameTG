from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards import reply_21, reply
from function_21 import get_card, list_card

message21_router = Router()


@message21_router.message(F.text == "🃏21")
async def rule_world(message: types.Message):
    await message.answer(
        text="Хотите ознакомиться с правилами игры?", reply_markup=reply_21.ready_21
    )


@message21_router.message(F.text == "📗 Правила")
async def rules(message: types.Message):
    await message.answer(
        text=f'Правила игры с ботом 🤖\n\n'
             f'1️⃣ Цель игры набрать больше очков чем вам соперник при этом не привысить 21 очко, тот кто первый наберет 21 очко, выиграет\n\n'
             f'2️⃣ В начале игры вам и диллеру(вашим диллером будет сам бот) будут выданы по одной карте из колоды карт. Колада состоит из 52 карт\n\n'
             f'3️⃣ Каждая ваша карта будет равна какому то очку\n'
             f'Туз – 11. Король – 4. Дама – 3. Валет – 2. Остальные по нумерованию самой карты.\n\n'
             f'4️⃣ В начале последующих ходов вам и диллеру будет даваться выбор взять еще одну карту или пропустить ход\n\n'
             f'5️⃣ Перед ходом вам и диллеру будут видны карты друг друга, всех кроме последней\n\n'
             f'6️⃣ Все очки ваших карт будут суммироваться и если при взятии карты вы привысите 21 очко вы проиграете, если очки привысит диллер програет он\n\n'
             f'7️⃣ Если оба игрока пропустят ход игра закончистя и выиграет тот кто больше набрал очков',
        reply_markup=reply_21.ready_p_21
    )


@message21_router.message(F.text == "Нaчaть!")
async def start_game(message: types.Message, state: FSMContext):
    await message.answer(
        text=f'С кем будете играть', reply_markup=reply_21.players
    )


@message21_router.message(F.text == "🤖 С ботом")
async def start_with_bot(message: types.Message, state: FSMContext):
    cards_bot = []
    cards_user = []
    cards1_user_key, cards1_user_value = get_card()
    cards_user.append(cards1_user_value)
    list_card.remove(cards1_user_key)
    card1_bot_key, card1_bot_value = get_card()
    cards_bot.append(card1_bot_value)
    list_card.remove(card1_bot_key)
    await message.answer(
        text=f'Вы и диллер получили карту:\n'
             f'Ваши карты\n'
             f'{cards1_user_key} = {cards1_user_value}'
    )
    await message.answer(
        text=f'Карты соперника:\n'
             f'?',
        reply_markup=reply_21.choosing_an_action
    )
    await state.update_data({
        "cards_bot": cards_bot,
        "cards_user": cards_user,
        "cards1_user_key": cards1_user_key,
        "card_values": list_card,
        "card1_bot_key": card1_bot_key,
        "cards1_user_value": cards1_user_value
    })
    await message.answer(text="Выберите действие", reply_markup=reply_21.choosing_an_action)
    await state.set_state("round2")


@message21_router.message(StateFilter('round2'))
async def round2(message: types.Message, state: FSMContext):
    if message.text == "Взять карту":
        data = await state.get_data()
        cards_bot2 = data.get("cards_bot")
        cards_user2 = data.get("cards_user")
        data.get("card_values")
        cards1_user_key = data.get("cards1_user_key")
        card1_bot_key = data.get("card1_bot_key")
        cards1_user_value = data.get("cards1_user_value")
        cards2_user_key, cards2_user_value = get_card()
        cards_user2.append(cards2_user_value)
        list_card.remove(cards2_user_key)
        card2_bot_key, card2_bot_value = get_card()
        cards_bot2.append(card2_bot_value)
        list_card.remove(card2_bot_key)
        await message.answer(
            text=f"Вы получили карту\n"
                 f"Ваши карты\n"
                 f"{cards1_user_key} = {cards1_user_value}\n"
                 f"{cards2_user_key} = {cards2_user_value}"
        )
        if sum(cards_user2) == 21:
            await message.answer(text=f"Вы набрали 21 очко\n"
                                      f"Вы выиграли",
                                 reply_markup=reply.game_selection
                                 )
            await state.clear()
        else:
            await message.answer(
                text=f'Диллер взял карту\n'
                     f'Карты соперника:\n'
                     f'{card1_bot_key}\n'
                     f'?',
                reply_markup=reply_21.choosing_an_action
            )
        if sum(cards_bot2) == 21:
            await message.answer(text=f"Диллер набрал 21 очко\n"
                                      f"Вы проиграли",
                                 reply_markup=reply.game_selection
                                 )
            await state.clear()
        else:
            await state.update_data({
                "cards_bot2": cards_bot2,
                "cards_user2": cards_user2,
                "cards2_user_key": cards2_user_key,
                "cards2_user_value": cards2_user_value,
                "card2_bot_key": card2_bot_key
            })
        await message.answer(text="Выберите действие", reply_markup=reply_21.choosing_an_action)
        await state.set_state("round3")
    elif message.text == "Пропустить ход":
        data = await state.get_data()
        cards_bot2 = data.get("cards_bot")
        cards_user2 = data.get("cards_user")
        data.get("card_values")
        cards1_user_key = data.get("cards1_user_key")
        cards1_user_value = data.get("cards1_user_value")
        card1_bot_key = data.get("card1_bot_key")
        card2_user_key = ""
        cards_user2.append(0)
        card2_bot_key, card2_bot_value = get_card()
        cards_bot2.append(card2_bot_value)
        list_card.remove(card2_bot_key)
        await message.answer(
            text=f"Диллер взял карту\n"
                 f"Ваши карты\n"
                 f"{cards1_user_key} = {cards1_user_value}"
        )
        await message.answer(
            text=f'Карты соперника:\n'
                 f'{card1_bot_key}\n'
                 f'?',
            reply_markup=reply_21.choosing_an_action
        )
        if sum(cards_bot2) == 21:
            await message.answer(text=f'Диллер набрал 21 очко\n'
                                      f'Вы проиграли',
                                 reply_markup=reply.game_selection
                                 )
            await message.answer(
                text=f'Карты диллера\n'
                     f'{card1_bot_key}\n'
                     f'{card2_bot_key}\n'
            )
            return await state.clear()
        else:
            await state.update_data({
                "cards_bot2": cards_bot2,
                "card2_bot_key": card2_bot_key,
                "card2_user_key": card2_user_key,
                "cards_user2": cards_user2
            })
        await message.answer(text="Выберите действие", reply_markup=reply_21.choosing_an_action)
        await state.set_state("round3")


@message21_router.message(StateFilter("round3"))
async def round3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cards_bot3 = data.get("cards_bot2")
    cards_user3 = data.get("cards_user2")
    data.get("card_values")
    cards1_user_key = data.get("cards1_user_key")
    cards2_user_key = data.get("cards2_user_key")
    card1_bot_key = data.get("card1_bot_key")
    card2_bot_key = data.get("card2_bot_key")
    cards1_user_value = data.get("cards1_user_value")
    cards2_user_value = data.get("cards2_user_value")
    if message.text == "Взять карту":
        cards3_user_key, cards3_user_value = get_card()
        cards_user3.append(cards3_user_value)
        list_card.remove(cards3_user_key)
        if sum(cards_bot3) < 17:
            card3_bot_key, card3_bot_value = get_card()
            cards_bot3.append(card3_bot_value)
            list_card.remove(card3_bot_key)
            bot_move = 1
        else:
            card3_bot_key, not_card3_bot_value = "", 0
            cards_bot3.append(not_card3_bot_value)
            bot_move = 0
        await message.answer(
            text=f"Вы получили карту\n"
                 f"Ваши карты\n"
                 f"{cards1_user_key} = {cards1_user_value}\n"
                 f"{cards2_user_key} = {cards2_user_value}\n"
                 f"{cards3_user_key} = {cards3_user_value}"
        )
        if sum(cards_user3) > 21:
            await message.answer(text=f"Вы набрали больше 21 очка\n"
                                      f"Вы проиграли",
                                 reply_markup=reply.game_selection
                                 )
            return await state.clear()
        elif sum(cards_user3) == 21:
            await message.answer(text=f"Вы набрали 21 очко\n"
                                      f"Вы выиграли",
                                 reply_markup=reply.game_selection
                                 )
            return await state.clear()
        else:
            if bot_move:
                if sum(cards_bot3) > 21:
                    await message.answer(text=f"Диллер привысил 21 очко\n"
                                              f"Вы победили!!",
                                         reply_markup=reply.game_selection
                                         )
                    await message.answer(
                        text=f'Карты диллера\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}'
                    )
                    return await state.clear()
                elif sum(cards_bot3) == 21:
                    await message.answer(text=f"Диллер набрал 21 очко\n"
                                              f"Вы проиграли!!",
                                         reply_markup=reply.game_selection
                                         )
                    await message.answer(
                        text=f'Карты диллера\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}'
                    )
                    return await state.clear()
                else:
                    await message.answer(
                        text=f'Диллел получил карту\n'
                             f'Карты соперника:\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'?',
                        reply_markup=reply_21.choosing_an_action
                    )
            elif bot_move == 0:
                await message.answer(
                    text=f'Диллер пропустил ход\n',
                    reply_markup=reply_21.choosing_an_action
                )
        await state.update_data({
            "cards_bot3": cards_bot3,
            "cards_user3": cards_user3,
            "cards3_user_key": cards3_user_key,
            "cards3_user_value": cards3_user_value,
            "card3_bot_key": card3_bot_key
        })
        await message.answer(text="Выберите действие", reply_markup=reply_21.choosing_an_action)
        await state.set_state("round4")
    elif message.text == "Пропустить ход":
        cards3_user_key, cards3_user_value = "Pass", 0
        cards_user3.append(cards3_user_value)
        data.get("card_values")
        if sum(cards_bot3) < 17:
            card3_bot_key, card3_bot_value = get_card()
            cards_bot3.append(card3_bot_value)
            list_card.remove(card3_bot_key)
            await message.answer(
                text=f"Диллер взял карту\n"
                     f"{card1_bot_key}\n"
                     f"{card2_bot_key}\n"
                     f"?"
            )
            if sum(cards_bot3) > 21:
                await message.answer(
                    text=f'Диллер набрал больше 21 очка\n'
                         f'Вы победили',
                    reply_markup=reply.game_selection
                )
                await message.answer(
                    text=f'Карты диллера\n'
                         f'{card1_bot_key}\n'
                         f'{card2_bot_key}\n'
                         f'{card3_bot_key}'
                )
                return await state.clear()
            elif sum(cards_bot3) == 21:
                await message.answer(
                    text=f'Диллер набрал 21 очко\n'
                         f'Вы проиграли',
                    reply_markup=reply.game_selection
                )
                await message.answer(
                    text=f'Карты диллера\n'
                         f'{card1_bot_key}\n'
                         f'{card2_bot_key}\n'
                         f'{card3_bot_key}'
                )
                return await state.clear()
            else:
                await message.answer(
                    text=f"Ваши карты\n"
                         f"{cards1_user_key} = {cards1_user_value}\n"
                         f"{cards2_user_key} = {cards2_user_value}\n",
                    reply_markup=reply_21.choosing_an_action
                )
            await state.update_data({
                "cards_bot3": cards_bot3,
                "cards_user3": cards_user3,
                "cards3_user_key": cards3_user_key,
                "cards3_user_value": cards3_user_value,
                "card3_bot_key": card3_bot_key
            })
            await message.answer(text="Ваш ход", reply_markup=reply_21.choosing_an_action)
            await state.set_state("round4")
        else:
            await message.answer(text="Диллер пропустил ход")
            if sum(cards_bot3) > sum(cards_user3):
                await message.answer(text=f"Диллер набрал больше очков = {sum(cards_bot3)}\n"
                                          f"Вы проиграли",
                                     reply_markup=reply.game_selection)
                return await state.clear()
            elif sum(cards_bot3) < sum(cards_user3):
                await message.answer(text=f"Вы набрали больше очков = {sum(cards_user3)}\n"
                                          f"Вы выиграли",
                                     reply_markup=reply.game_selection)
                return await state.clear()
            else:
                await message.answer(text=f"У вас с диллерои равные очки = {sum(cards_bot3)}\n"
                                          f"Ничья",
                                     reply_markup=reply.game_selection)
                return await state.clear()


@message21_router.message(StateFilter("round4"))
async def round4(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cards_bot4 = data.get("cards_bot3")
    cards_user4 = data.get("cards_user3")
    data.get("card_values")
    cards1_user_key = data.get("cards1_user_key")
    cards2_user_key = data.get("cards2_user_key")
    cards3_user_key = data.get("cards3_user_key")
    card1_bot_key = data.get("card1_bot_key")
    card2_bot_key = data.get("card2_bot_key")
    card3_bot_key = data.get("card3_bot_key")
    cards1_user_value = data.get("cards1_user_value")
    cards2_user_value = data.get("cards2_user_value")
    cards3_user_value = data.get("cards3_user_value")
    if message.text == "Взять карту":
        cards4_user_key, cards4_user_value = get_card()
        cards_user4.append(cards4_user_value)
        list_card.remove(cards4_user_key)
        if sum(cards_bot4) < 17:
            card4_bot_key, card4_bot_value = get_card()
            cards_bot4.append(card4_bot_value)
            list_card.remove(card4_bot_key)
        else:
            card4_bot_key, not_card4_bot_value = "", 0
            cards_bot4.append(not_card4_bot_value)
        await message.answer(
            text=f"Вы получили карту\n"
                 f"Ваши карты\n"
                 f"{cards1_user_key} = {cards1_user_value}\n"
                 f"{cards2_user_key} = {cards2_user_value}\n"
                 f"{cards3_user_key} = {cards3_user_value}\n"
                 f"{cards4_user_key} = {cards4_user_value}"
        )
        if sum(cards_user4) > 21:
            await message.answer(text=f"Вы набрали больше 21 очка\n"
                                      f"Вы проиграли",
                                 reply_markup=reply.game_selection
                                 )
            return await state.clear()
        elif sum(cards_user4) == 21:
            await message.answer(text=f"Вы набрали 21 очко\n"
                                      f"Вы выиграли",
                                 reply_markup=reply.game_selection
                                 )
            return await state.clear()
        else:
            if 0 not in cards_bot4:
                if sum(cards_bot4) > 21:
                    await message.answer(text=f"Диллер привысил 21 очко\n"
                                              f"Вы победили!!",
                                         reply_markup=reply.game_selection
                                         )
                    await message.answer(
                        text=f'Карты диллера\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}\n'
                             f'{card4_bot_key}'
                    )
                    return await state.clear()
                elif sum(cards_bot4) == 21:
                    await message.answer(text=f"Диллер набрал 21 очко\n"
                                              f"Вы проиграли!!",
                                         reply_markup=reply.game_selection
                                         )
                    await message.answer(
                        text=f'Карты диллера\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}\n'
                             f'{card4_bot_key}'
                    )
                    return await state.clear()
                else:
                    await message.answer(
                        text=f'Диллел получил карту\n'
                             f'Карты соперника:\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}\n'
                             f'?',
                        reply_markup=reply_21.choosing_an_action
                    )
            else:
                await message.answer(
                    text=f'Диллер пропустил ход\n',
                    reply_markup=reply_21.choosing_an_action
                )
        await state.update_data({
            "cards_bot4": cards_bot4,
            "cards_user4": cards_user4,
            "cards4_user_key": cards4_user_key,
            "cards4_user_value": cards4_user_value,
            "card4_bot_key": card4_bot_key
        })
        await message.answer(text="Выберите действие", reply_markup=reply_21.choosing_an_action)
        await state.set_state("round5")
    elif message.text == "Пропустить ход":
        cards4_user_key, cards4_user_value = "Pass", 0
        cards_user4.append(cards4_user_value)
        if sum(cards_bot4) < 17:
            card4_bot_key, card4_bot_value = get_card()
            cards_bot4.append(card4_bot_value)
            list_card.remove(card4_bot_key)
            await message.answer(
                text=f"Диллер взял карту\n"
                     f"{card1_bot_key}\n"
                     f"{card2_bot_key}\n"
                     f"{card3_bot_key}"
                     f"?"
            )
            if sum(cards_bot4) > 21:
                await message.answer(
                    text=f'Диллер набрал больше 21 очка\n'
                         f'Вы победили',
                    reply_markup=reply.game_selection
                )
                await message.answer(
                    text=f'Карты диллера\n'
                         f'{card1_bot_key}\n'
                         f'{card2_bot_key}\n'
                         f'{card3_bot_key}\n'
                         f'{card4_bot_key}'
                )
                return await state.clear()
            elif sum(cards_bot4) == 21:
                await message.answer(
                    text=f'Диллер набрал 21 очко раньше вас\n'
                         f'Вы проиграли',
                    reply_markup=reply.game_selection
                )
                await message.answer(
                    text=f'Карты диллера\n'
                         f'{card1_bot_key}\n'
                         f'{card2_bot_key}\n'
                         f'{card3_bot_key}\n'
                         f'{card4_bot_key}'
                )
                return await state.clear()
            else:
                await message.answer(
                    text=f"Ваши карты\n"
                         f"{cards1_user_key} = {cards1_user_value}\n"
                         f"{cards2_user_key} = {cards2_user_value}\n"
                         f"{cards3_user_key} = {cards3_user_value}",
                    reply_markup=reply_21.choosing_an_action
                )
            await state.update_data({
                "cards_bot4": cards_bot4,
                "cards_user4": cards_user4,
                "cards4_user_key": cards4_user_key,
                "cards4_user_value": cards4_user_value,
                "card4_bot_key": card4_bot_key
            })
            await message.answer(text="Ваш ход", reply_markup=reply_21.choosing_an_action)
            await state.set_state("round5")
        else:
            await message.answer(text="Диллер пропустил ход")
            if sum(cards_bot4) > sum(cards_user4):
                await message.answer(text=f"Диллер набрал больше очков = {sum(cards_bot4)}\n"
                                          f"Вы проиграли",
                                     reply_markup=reply.game_selection)
                return await state.clear()
            elif sum(cards_bot4) < sum(cards_user4):
                await message.answer(text=f"Вы набрали больше очков = {sum(cards_user4)}\n"
                                          f"Вы выиграли",
                                     reply_markup=reply.game_selection)
                return await state.clear()
            else:
                await message.answer(text=f"У вас с диллерои равные очки = {sum(cards_bot4)}\n"
                                          f"Ничья",
                                     reply_markup=reply.game_selection)
                return await state.clear()


@message21_router.message(StateFilter("round5"))
async def round5(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cards_bot5 = data.get("cards_bot4")
    cards_user5 = data.get("cards_user4")
    data.get("card_values")
    cards1_user_key = data.get("cards1_user_key")
    cards2_user_key = data.get("cards2_user_key")
    cards3_user_key = data.get("cards3_user_key")
    cards4_user_key = data.get("cards4_user_key")
    card1_bot_key = data.get("card1_bot_key")
    card2_bot_key = data.get("card2_bot_key")
    card3_bot_key = data.get("card3_bot_key")
    card4_bot_key = data.get("card4_bot_key")
    cards1_user_value = data.get("cards1_user_value")
    cards2_user_value = data.get("cards2_user_value")
    cards3_user_value = data.get("cards3_user_value")
    cards4_user_value = data.get("cards4_user_value")
    if message.text == "Взять карту":
        cards5_user_key, cards5_user_value = get_card()
        cards_user5.append(cards5_user_value)
        list_card.remove(cards5_user_key)
        if sum(cards_bot5) < 17:
            card5_bot_key, card5_bot_value = get_card()
            cards_bot5.append(card5_bot_value)
            list_card.remove(card5_bot_key)
        else:
            card5_bot_key, not_card5_bot_value = "", 0
            cards_bot5.append(not_card5_bot_value)
        await message.answer(
            text=f"Вы получили карту\n"
                 f"Ваши карты\n"
                 f"{cards1_user_key} = {cards1_user_value}\n"
                 f"{cards2_user_key} = {cards2_user_value}\n"
                 f"{cards3_user_key} = {cards3_user_value}\n"
                 f"{cards4_user_key} = {cards4_user_value}\n"
                 f"{cards5_user_key} = {cards5_user_value}"
        )
        if sum(cards_user5) > 21:
            await message.answer(text=f"Вы набрали больше 21 очка\n"
                                      f"Вы проиграли",
                                 reply_markup=reply.game_selection
                                 )
            return await state.clear()
        elif sum(cards_user5) == 21:
            await message.answer(text=f"Вы набрали 21 очко\n"
                                      f"Вы выиграли",
                                 reply_markup=reply.game_selection
                                 )
            return await state.clear()
        else:
            if 0 not in cards_bot5:
                if sum(cards_bot5) > 21:
                    await message.answer(text=f"Диллер привысил 21 очко\n"
                                              f"Вы победили!!",
                                         reply_markup=reply.game_selection
                                         )
                    await message.answer(
                        text=f'Карты диллера\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}\n'
                             f'{card4_bot_key}\n'
                             f'{card5_bot_key}'
                    )
                    return await state.clear()
                elif sum(cards_bot5) == 21:
                    await message.answer(text=f"Диллер набрал 21 очко\n"
                                              f"Вы проиграли!!",
                                         reply_markup=reply.game_selection
                                         )
                    await message.answer(
                        text=f'Карты диллера\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}\n'
                             f'{card4_bot_key}\n'
                             f'{card5_bot_key}'
                    )
                    return await state.clear()
                else:
                    await message.answer(
                        text=f'Диллел получил карту\n'
                             f'Карты соперника:\n'
                             f'{card1_bot_key}\n'
                             f'{card2_bot_key}\n'
                             f'{card3_bot_key}\n'
                             f'?',
                        reply_markup=reply_21.choosing_an_action
                    )
            else:
                await message.answer(
                    text=f'Диллер пропустил ход\n',
                    reply_markup=reply_21.choosing_an_action
                )
        await state.update_data({
            "cards_bot5": cards_bot5,
            "cards_user5": cards_user5,
            "cards5_user_key": cards5_user_key,
            "cards5_user_value": cards5_user_value,
            "card5_bot_key": card5_bot_key
        })
        await message.answer(text="Выберите действие", reply_markup=reply_21.choosing_an_action)
        await state.set_state("round5")
    elif message.text == "Пропустить ход":
        cards5_user_key, cards5_user_value = "Pass", 0
        cards_user5.append(cards5_user_value)
        if sum(cards_bot5) < 17:
            card5_bot_key, card5_bot_value = get_card()
            cards_bot5.append(card5_bot_value)
            list_card.remove(card5_bot_key)
            await message.answer(
                text=f"Диллер взял карту\n"
                     f"{card1_bot_key}\n"
                     f"{card2_bot_key}\n"
                     f"{card3_bot_key}\n"
                     f"{card4_bot_key}\n"
                     f"?"
            )
            if sum(cards_bot5) > 21:
                await message.answer(
                    text=f'Диллер набрал больше 21 очка\n'
                         f'Вы победили',
                    reply_markup=reply.game_selection
                )
                await message.answer(
                    text=f'Карты диллера\n'
                         f'{card1_bot_key}\n'
                         f'{card2_bot_key}\n'
                         f'{card3_bot_key}\n'
                         f'{card4_bot_key}\n'
                         f'{card5_bot_key}'
                )
                return await state.clear()
            elif sum(cards_bot5) == 21:
                await message.answer(
                    text=f'Диллер набрал 21 очко раньше вас\n'
                         f'Вы проиграли',
                    reply_markup=reply.game_selection
                )
                await message.answer(
                    text=f'Карты диллера\n'
                         f'{card1_bot_key}\n'
                         f'{card2_bot_key}\n'
                         f'{card3_bot_key}\n'
                         f'{card4_bot_key}\n'
                         f'{card5_bot_key}'
                )
                return await state.clear()
            else:
                await message.answer(
                    text=f"Ваши карты\n"
                         f"{cards1_user_key} = {cards1_user_value}\n"
                         f"{cards2_user_key} = {cards2_user_value}\n"
                         f"{cards3_user_key} = {cards3_user_value}\n"
                         f"{cards4_user_key} = {cards4_user_value}",
                    reply_markup=reply_21.choosing_an_action
                )
            await state.update_data({
                "cards_bot5": cards_bot5,
                "cards_user5": cards_user5,
                "cards5_user_key": cards5_user_key,
                "cards5_user_value": cards5_user_value,
                "card5_bot_key": card5_bot_key
            })
            await message.answer(text="Ваш ход", reply_markup=reply_21.choosing_an_action)
            await state.set_state("round5")
        else:
            await message.answer(text="Диллер пропустил ход")
            if sum(cards_bot5) > sum(cards_user5):
                await message.answer(text=f"Диллер набрал больше очков = {sum(cards_bot5)}\n"
                                          f"Вы проиграли",
                                     reply_markup=reply.game_selection)
                return await state.clear()
            elif sum(cards_bot5) < sum(cards_user5):
                await message.answer(text=f"Вы набрали больше очков = {sum(cards_user5)}\n"
                                          f"Вы выиграли",
                                     reply_markup=reply.game_selection)
                return await state.clear()
            else:
                await message.answer(text=f"У вас с диллерои равные очки = {sum(cards_bot5)}\n"
                                          f"Ничья",
                                     reply_markup=reply.game_selection)
                return await state.clear()
