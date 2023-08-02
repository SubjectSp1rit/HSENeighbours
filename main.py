from aiogram.utils import executor
from initialise import dispatcher
from client import client_handlers
import datetime


async def on_startup(_):
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{str(datetime.datetime.now())[:-7]}')
        f.write(' Бот запущен')

client_handlers(dispatcher)

executor.start_polling(dispatcher,
                       skip_updates=True,
                       on_startup=on_startup)
