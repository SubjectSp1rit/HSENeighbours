from aiogram import types, Dispatcher
from initialise import bot, dispatcher
from keyboard import inline_keyboard_start, keyboard_menu, keyboard_dormitory_or_flat
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import sqlite3 as sq
import asyncio


async def db_start():
    global db, cur

    db = sq.connect('database.db')
    cur = db.cursor()

# -----------------------------------

class FSM_flat(StatesGroup):
    name = State()
    desc = State()


async def name(message: types.Message, state: FSMContext):
    answer_name = message.text
    await state.update_data(answer1=answer_name)

    await bot.send_message(message.from_user.id,
                           'Укажите дополнительную информацию. Например, это может быть желаемое метро/количество людей/etc. Любая информация очень ценна для соискателя.')
    await FSM_flat.next()


async def desc(message: types.Message, state: FSMContext):
    answer_desc = message.text
    await state.update_data(answer2=answer_desc)

    data = await state.get_data()
    name, desc = data.get('answer1'), data.get('answer2')

    user_id = cur.execute(f"SELECT 1 FROM looking_for_flat WHERE telegram_id == '{message.from_user.id}'").fetchall()
    if user_id:
        try:
            cur.execute(
                f"UPDATE looking_for_flat SET telegram_id = '{message.from_user.id}', telegram_tag = '{message.from_user.username}', FI = '{name}', description = '{desc}'")
            db.commit()
            await bot.send_message(message.from_user.id,
                                   'Информация успешно обновлена!',
                                   reply_markup=keyboard_menu)
        except Exception:
            await bot.send_message(message.from_user.id,
                                   'Произошла неизвестная ошибка.')
    else:
        try:
            cur.execute(
                f"INSERT INTO looking_for_flat(telegram_id, telegram_tag, FI, description) VALUES('{message.from_user.id}', '{message.from_user.username}', '{name}', '{desc}')")
            db.commit()
            await bot.send_message(message.from_user.id,
                                   'Информация успешно добавлена!',
                                   reply_markup=keyboard_menu)
        except Exception:
            await bot.send_message(message.from_user.id,
                                   'Произошла неизвестная ошибка.')
    await state.finish()


# ------------------------------------

class FSM(StatesGroup):
    dormitory_id = State()
    room_id = State()
    FI = State()


async def dormitory(message: types.Message, state: FSMContext):
    answer_dormitory = message.text
    await state.update_data(answer1=answer_dormitory)

    await bot.send_message(message.from_user.id,
                           'Укажите номер комнаты так, как указано на почте (без цифры внутри скобок)')
    await FSM.next()


async def room(message: types.Message, state: FSMContext):
    answer_room = message.text
    await state.update_data(answer2=answer_room)

    await bot.send_message(message.from_user.id,
                           'Укажите свою фамилию и имя')
    await FSM.next()


async def FI(message: types.Message, state: FSMContext):
    answer_FI = message.text
    await state.update_data(answer3=answer_FI)

    data = await state.get_data()
    dormitory_id, room_id, fi = data.get('answer1'), data.get('answer2'), data.get('answer3')
    if dormitory_id.isdigit() and room_id.isdigit() and (not fi.isdigit()):
        user_id = cur.execute(f"SELECT 1 FROM users WHERE telegram_id == '{message.from_user.id}'").fetchall()
        if user_id:
            cur.execute(f"DELETE FROM users WHERE telegram_id == '{message.from_user.id}'")
            db.commit()
            try:
                cur.execute(
                    f"INSERT INTO users(telegram_id, telegram_tag, dormitory_id, room_id, FI) VALUES('{message.from_user.id}', '{message.from_user.username}', '{dormitory_id}', '{room_id}', '{fi}')")
                db.commit()
                await bot.send_message(message.from_user.id,
                                       'Информация успешно обновлена!',
                                       reply_markup=keyboard_menu)
            except Exception:
                await bot.send_message(message.from_user.id,
                                       'Произошла неизвестная ошибка.')
        else:
            try:
                cur.execute(f"INSERT INTO users(telegram_id, telegram_tag, dormitory_id, room_id, FI) VALUES('{message.from_user.id}', '{message.from_user.username}', '{dormitory_id}', '{room_id}', '{fi}')")
                db.commit()
                await bot.send_message(message.from_user.id,
                                       'Информация успешно добавлена!',
                                       reply_markup=keyboard_menu)
            except Exception:
                await bot.send_message(message.from_user.id,
                                 'Произошла неизвестная ошибка.')
    else:
        await bot.send_message(message.from_user.id,
                               'Что-то пошло не так. Проверьте корректность введенных данных и попробуйте снова.',
                               reply_markup=keyboard_menu)
    await state.finish()

# ---------------------------


async def send_message(message: types.message):
    if message.text.lower() == 'добавить/изменить информацию о себе':
        await bot.send_message(message.from_user.id,
                               'Пожалуйста, нажмите одну из кнопок ниже.',
                               reply_markup=keyboard_dormitory_or_flat)
    elif message.text.lower() == 'добавить информацию об общежитии':
        await bot.send_message(message.from_user.id,
                               'Укажите номер общежития цифрой (без доп. знаков)')
        await FSM.dormitory_id.set()

    elif message.text.lower() == 'добавить информацию о поиске квартиры':
        await bot.send_message(message.from_user.id,
                               'Укажите свою фамилию и имя')
        await FSM_flat.name.set()

    elif message.text.lower() == 'вернуться в меню':
        await bot.send_message(message.from_user.id,
                               'Вы вернулись в главное меню.',
                               reply_markup=keyboard_menu)
    elif message.text.lower() == 'найти соседей в общежитии':
        dor_id = cur.execute(f"SELECT dormitory_id FROM users WHERE telegram_id = '{message.from_user.id}'").fetchone()[0]
        rom_id = cur.execute(f"SELECT room_id FROM users WHERE telegram_id = '{message.from_user.id}'").fetchone()[0]
        answer = 'С вами в комнате живут:'
        neighbours = cur.execute(f"SELECT * FROM users WHERE dormitory_id = '{dor_id}' AND room_id = '{rom_id}'").fetchall()

        async def f(l: list):
            for x in l:
                yield x

        async for elem in f(neighbours):
            answer += '\n' + elem[5] + f', его/её тг: @{elem[2]}'

        answer += '\n\n' + 'Все жители вашего общежития:'
        neighbours = cur.execute(f"SELECT * FROM users WHERE dormitory_id = '{dor_id}'").fetchall()
        async for elem in f(neighbours):
            answer += '\n' + elem[5] + f', его/её тг: @{elem[2]}'

        await bot.send_message(message.from_user.id,
                               f'{answer}')

    elif message.text.lower() == 'показать людей, желающих снять квартиру с кем-то':
        flats = cur.execute(f"SELECT * FROM looking_for_flat").fetchall()
        answer = ''
        async def f(l: list):
            for x in l:
                yield x

        async for elem in f(flats):
            answer += elem[3] + f', его/её тг: @{elem[2]}' + '\n'
            answer += elem[4] + '\n\n'

        await bot.send_message(message.from_user.id,
                               answer)


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

async def menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы попали в меню.\nПожалуйста, воспользуйтесь кнопками ниже.',
                           reply_markup=keyboard_menu)


def client_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(callback=menu)

    dp.register_message_handler(send_message, state=None)

    dp.register_message_handler(dormitory, state=FSM.dormitory_id)
    dp.register_message_handler(room, state=FSM.room_id)
    dp.register_message_handler(FI, state=FSM.FI)

    dp.register_message_handler(name, state=FSM_flat.name)
    dp.register_message_handler(desc, state=FSM_flat.desc)
