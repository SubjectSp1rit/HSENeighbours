from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard_start = InlineKeyboardMarkup(row_width=1)
menubutton = InlineKeyboardButton(text='Меню', callback_data='/Меню')
inline_keyboard_start.add(menubutton)

# -----------------------------------------

keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_add_info = KeyboardButton('Добавить/изменить информацию о себе')
button_find_dormitory_neighbours = KeyboardButton('Найти соседей в общежитии')
button_find_flat = KeyboardButton('Показать людей, желающих снять квартиру с кем-то')
keyboard_menu.add(button_add_info).add(button_find_dormitory_neighbours).add(button_find_flat)

# ------------------------------------------

keyboard_dormitory_or_flat = ReplyKeyboardMarkup(resize_keyboard=True)
button_dormitory = KeyboardButton('Добавить информацию об общежитии')
button_flat = KeyboardButton('Добавить информацию о поиске квартиры')
button_main = KeyboardButton('Вернуться в меню')
keyboard_dormitory_or_flat.add(button_flat).add(button_dormitory).add(button_main)

