import asyncio
from aiogram import Bot, Dispatcher

from handlers import command_wordle, message_wordle, commands, message_21, password, roulette
from handlers_online import message_21_on
from aiogram.client.default import DefaultBotProperties


async def main():
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token="6439053673:AAFMAn-dNZQjd2WLHD4s6kyxC1v9X9yl-_w", default=default)
    # bot = Bot("6439053673:AAFMAn-dNZQjd2WLHD4s6kyxC1v9X9yl-_w")
    dp = Dispatcher()
    dp.include_routers(
        message_wordle.messageWordle_router,
        command_wordle.commandWordle_router,
        commands.commands_router,
        message_21.message21_router,
        password.password_router,
        roulette.roulette_router,
        message_21_on.message21on_router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())