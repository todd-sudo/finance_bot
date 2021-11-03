<h2>Telegram бот для учёта личных расходов и ведения бюджет</h2>


В переменных окружения надо проставить API токен бота и свой ID в телеграме

`TELEGRAM_API_TOKEN` — API токен бота

`TELEGRAM_ACCESS_ID` — ID Telegram аккаунта, от которого будут приниматься сообщения (сообщения от остальных аккаунтов игнорируются)


Создаем виртуальное окружение, затем активируем его:

`python3 -m venv env`
`sourse env/bin/activate`

Устанавливаем зависимости:

`pip install -r pip-requirements.txt`


Устанавливаем дополнительные пакеты:

`pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3`


Создаем папку `db` . В ней создаем файл `finance.db`


Запускаем основной файл:

`python server.py`
