from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard_start = InlineKeyboardMarkup(row_width=1)
menubutton = InlineKeyboardButton(text='Меню', callback_data='/Меню')
inline_keyboard_start.add(menubutton)