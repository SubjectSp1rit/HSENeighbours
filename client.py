from aiogram import types, Dispatcher
from initialise import bot
from keyboard import inline_keyboard_start
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


async def send_message(message: types.message):
    if message.text.lower() == 'привет':
        await message.reply('Привет')


async def start(message: types.Message):
    if message.from_user.first_name and message.from_user.last_name:
        await bot.send_message(message.from_user.id,
                               f'Приветствую, {message.from_user.first_name} {message.from_user.last_name}!',
                               reply_markup=inline_keyboard_start)
    elif message.from_user.first_name and (not message.from_user.last_name): \
        await bot.send_message(message.from_user.id,
                               f'Приветствую, {message.from_user.first_name}!',
                               reply_markup=inline_keyboard_start)
    else:
        await bot.send_message(message.from_user.id,
                               f'Приветствую, {message.from_user.last_name}!',
                               reply_markup=inline_keyboard_start)


def client_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

    dp.register_message_handler(send_message, state=None)
