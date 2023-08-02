from aiogram.utils import executor
from initialise import dispatcher
from client import client_handlers
import aiofiles
import datetime
from client import db_start


async def on_startup(_):
    await db_start()
    async with aiofiles.open(file='log.txt', mode='a', encoding='utf-8') as f:
        await f.write(f'\n{str(datetime.datetime.now())[:-7]} Бот запущен успешно')


async def on_shutdown(_):
    async with aiofiles.open(file='log.txt', mode='a', encoding='utf-8') as f:
        await f.write(f'\n{str(datetime.datetime.now())[:-7]} Бот выключен')

client_handlers(dispatcher)

executor.start_polling(dispatcher,
                       skip_updates=True,
                       on_startup=on_startup,
                       on_shutdown=on_shutdown)
