from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

message21on_router = Router()


@message21on_router.message(F.text == "🫂 С Другом")
async def start_with_bot(message: types.Message, state: FSMContext):
    await message.answer(text="Пока не доступно")