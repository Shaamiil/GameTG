import asyncio
from aiogram import Bot, Dispatcher

from handlers import command_wordle, message_wordle, commands, message_21, password


async def main():
    bot = Bot("6439053673:AAFMAn-dNZQjd2WLHD4s6kyxC1v9X9yl-_w")
    dp = Dispatcher()
    dp.include_routers(
        message_wordle.messageWordle_router,
        command_wordle.commandWordle_router,
        commands.commands_router,
        message_21.message21_router,
        password.password_router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())