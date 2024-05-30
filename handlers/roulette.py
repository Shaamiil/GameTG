import random

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards import reply_roulette
from function_roulette import create_cartridges

roulette_router = Router()
game_state = {}


@roulette_router.message(F.text == "🩸 Buckshot Roulette")
async def rule_roulette(message: types.Message):
    await message.answer(
        text="Игра еще в разработке"
    )
# reply_markup=reply_roulette.players

@roulette_router.message(F.text == "📕 Правила")
async def rules(message: types.Message):
    await message.answer(
        text=f'Правила игры с ботом 🤖\n\n'
             f'1️⃣ Чтобы победить в этой игре нужно одолеть бота в трех раундах\n\n'
             f'2️⃣ В каждом раунде у вас с ботом будет одинаковое количество жизней и раунд не закончистя '
             f'пока у одного из игроков они не закочатся\n\n'
             f'3️⃣ В начале кажодго раунда вы будете начинать игру и вам будет показано сколько в ружье пустых '
             f'гильз и сколько боевых\n\n'
             f'4️⃣ Если патроны закончились раньше чем жизни, то патроны в ружье обновлятся и '
             f'вы снова начинаете игру\n\n'
             f'5️⃣ Ваша задача решить в кого вы будете стрелять в себя или в бота\n\n'
             f'6️⃣ Если вы выстрелите в себя пустым патроном бот пропустит ход и вы снова решаете в кого стрелять,'
             f' это же правило касается и бота\n\n'
             f'7️⃣ В остальных случаях ход переходит другому игроку',
        reply_markup=reply_roulette.ready_p_roulette
    )


@roulette_router.message(F.text == "Hачать!")
async def start_game(message: types.Message, state: FSMContext):
    await message.answer(
        text=f'С кем будете играть', reply_markup=reply_roulette.shoot
    )


@roulette_router.message(F.text == "🤖 С бoтoм")
async def start_with_bot(message: types.Message, state: FSMContext):
    await message.answer(text="Начинаем?", reply_markup=reply_roulette.ready_p_roulette)
    await state.set_state("game")


@roulette_router.message(StateFilter("game"))
async def game(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name

