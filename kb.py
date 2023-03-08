from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from professional import PROFESSIONALS_LIST_RU

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(KeyboardButton("Присоединиться к игре"), KeyboardButton("Создать игру"))

kb_start_game = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_game.add(KeyboardButton("Начать игру"), KeyboardButton("Удалить игру"))

kb_exit_game = ReplyKeyboardMarkup(resize_keyboard=True)
kb_exit_game.add(KeyboardButton("Выйти из игры"))

kb_game = ReplyKeyboardMarkup(resize_keyboard=True)
kb_game.add(KeyboardButton("День выплат"),
            KeyboardButton("Статистика"),
            KeyboardButton("Купить акции"),
            KeyboardButton("Продать акции"),
            KeyboardButton("Купить недвижимость"),
            KeyboardButton("Продать недвижимость"),
            KeyboardButton("Добавить золотые монеты"),
            KeyboardButton("Обменять золотое монеты"),
            KeyboardButton("Всякая всячина"),
            KeyboardButton("Взять кредит"),
            KeyboardButton("Частично погасить банковский кредит"),
            KeyboardButton("Погасить не банковский кредит"),
            KeyboardButton("Добавить ребенка"),
            )


