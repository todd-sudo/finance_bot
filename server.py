"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os
import exceptions
import expenses

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, bold, italic, code, pre
from keyboards import keyboard_start_help
from categories import Categories
from middlewares import AccessMiddleware

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    first_msg = text(bold("Бот для учёта финансов"))
    today_msg = text(code("Сегодняшняя статистика:"), bold("/today"))
    month_msg = text(code("За текущий месяц:"), bold("/month"))
    expenses_msg = text(code("Последнии внесённые расходы:"), bold("/expenses"))
    categories_msg = text(code("Категории трат:"), bold("/categories"))
    add_finance_msg = text(bold("Чтобы добавить расход:"), italic("250 такси"))

    msg = f"{first_msg}\n\n{today_msg}\n" \
          f"{month_msg}\n" \
          f"{expenses_msg}\n" \
          f"{categories_msg}\n\n" \
          f"{add_finance_msg}"

    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    try:
        row_id = int(message.text[4:])
        expenses.delete_expense(row_id)
        answer_message = "Удалил"
        await message.answer(answer_message)
    except ValueError:
        await message.answer('Я не смог удалить! Повтори позже')


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " + \
                     ("\n* ".join(
                         [c.name + ' (' + ", ".join(c.aliases) + ')' for c in
                          categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* " \
        .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message) -> None:
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
