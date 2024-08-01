from aiogram import Bot, Dispatcher, Router
from dotenv import dotenv_values

config_key = dotenv_values('.env')

bot = Bot(token='7140801194:AAFtC1biMQKqe7ybgBS3hhddFUfWnOE0dxk')
dp = Dispatcher()


TRELLO_API_KEY = config_key['TRELLO_API_KEY']
TRELLO_API_SECRET = config_key['TRELLO_API_SECRET']
TRELLO_TOKEN = config_key['TRELLO_TOKEN']
TRELLO_BOARD_ID = config_key['TRELLO_BOARD_ID']