"""Кнопки для бота, для быстрого ввода команд"""

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_categories = KeyboardButton('/categories')
button_today = KeyboardButton('/today')
button_month = KeyboardButton('/month')
button_expenses = KeyboardButton('/expenses')
button_help = KeyboardButton('/help')

keyboard_start_help = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=False)

keyboard_start_help.add(button_categories, button_today, button_month)
keyboard_start_help.add(button_expenses, button_help)


