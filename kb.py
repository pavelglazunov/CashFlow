from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
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

kb_deal = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton("мелкая сделка")).insert(
    KeyboardButton("крупная сделка"))

kb_deal_l2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_deal_l2.insert(KeyboardButton("сетевой маркетинг"))
kb_deal_l2.insert(KeyboardButton("монеты и долг"))
kb_deal_l2.insert(KeyboardButton("недвижимость"))
kb_deal_l2.insert(KeyboardButton("акции"))


def kb_game_menu(session):
    kb_game_menu = InlineKeyboardMarkup(row_width=3)
    kb_game_menu.insert(InlineKeyboardButton("✴️ день выплат ✴️", callback_data=f"#pd;{session}"))
    kb_game_menu.row(InlineKeyboardButton("🆘 всякая всячина 🆘", callback_data=f"#vv;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("✅ сделка ✅", callback_data=f"#dl;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🌐 рынок 🌐", callback_data=f"#mk;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🚺 благотворительность 🚺", callback_data=f"#ct;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🚹 ребенок 🚹", callback_data=f"#cl;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🛂 увольнение 🛂", callback_data=f"#dm;{session}"))

    return kb_game_menu
