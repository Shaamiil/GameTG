from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards import reply

commands_router = Router()

@commands_router.message(Command("start"))
async def game(message: types.Message):
    await message.answer(
        text=f'Внимание ‼️\nБот еще в разработке\nВозможны некие неполадки)',
        reply_markup=reply.play
    )