from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(KeyboardButton("Присоединиться к игре"), KeyboardButton("Создать игру"))


kb_start_game = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_game.add(KeyboardButton("Начать игру"), KeyboardButton("Удалить игру"))

kb_exit_game = ReplyKeyboardMarkup(resize_keyboard=True)
kb_exit_game.add(KeyboardButton("Выйти из игры"))
