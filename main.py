from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from kb import *
from session import create_session, join_session, check_user_active_game, get_session_players, exit_from_session, \
    remove_session, get_session_by_admin
from functions import validate_token
from forms import StartGame, JoinGame, RemoveGame

TOKEN = "6083708114:AAFAUp-Pads5YI-jS8FOgG4U4oJzkonBUlE"

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в CashFlow bot, укадите необходимое действие", reply_markup=kb_start)


@dp.message_handler(state=StartGame.start)
async def create_game(message: types.Message, state: FSMContext):
    if message.text == "0":
        await state.finish()
        return

    if validate_token(message.text.lower()):

        session_answer = create_session(message.from_user.id, message.text.lower())
        if not session_answer:
            await message.answer("Сессия успешно создана, используйте ваш токен, чтобы пригласить друзей",
                                 reply_markup=kb_start_game)
            await state.finish()
            return
        await message.answer(session_answer)
        return
    await message.answer("Некоректный токен, введите другой")
    return


@dp.message_handler(state=JoinGame.token)
async def join_game(message: types.Message, state: FSMContext):
    if message.text == "0":
        await state.finish()
        return

    if validate_token(message.text.lower()):
        session_answer = join_session(message.text.lower(), message.from_user.id)

        if not session_answer:
            await message.answer("Вы успешно вступили в игру, ожидайте начала", reply_markup=kb_exit_game)

            for u in get_session_players(message.text.lower()):
                if u != str(message.from_user.id):
                    await bot.send_message(u, f"Игрок {message.from_user.username} присоединился к игре")
            await state.finish()
            return

        await message.answer(session_answer)
    return


@dp.message_handler(state=RemoveGame.token)
async def remove_game(message: types.Message, state: FSMContext):
    if message.text == "0":
        await state.finish()
        return

    if validate_token(message.text.lower()):
        status, session_users = remove_session(message.text.lower(), message.from_user.id)

        if session_users:
            await state.finish()

        for i in session_users:
            await bot.send_message(i, "Игра была удалена, вы были перенаправлены в главное меню", reply_markup=kb_start)
    return


@dp.message_handler()
async def all_message(message: types.Message):
    if message.text == "Присоединиться к игре":
        status = check_user_active_game(message.from_user.id)
        if status:
            await message.answer(status)
            return
        await message.answer("Введите токен игры или 0 для отмены")
        await JoinGame.token.set()
    if message.text == "Создать игру":
        status = check_user_active_game(message.from_user.id)
        if status:
            await message.answer(status)
            return
        await message.answer("Введите токен, по которому игроки смогут присоединиться к игре "
                             "(токен должен состоять не менее чем из 6 символов и только из английских букв)"
                             " или 0 для отмены")
        await StartGame.start.set()
    if message.text == "Выйти из игры":
        answer = exit_from_session(message.from_user.id)
        await message.answer(answer[0], reply_markup=kb_start)
        if answer[1]:
            for i in get_session_players(answer[1]):
                await bot.send_message(i, f"Пользователь {message.from_user.username} вышел из игры",
                                       reply_markup=kb_start)
    if message.text == "Удалить игру":
        await message.answer("Введите токен игры для подтверждения или 0 для отмены")
        await RemoveGame.token.set()
    if message.text == "Начать игру":
        if session := get_session_by_admin(message.from_user.id):
            for i in session[1]:
                await bot.send_message(i, "Начало игры, укажите вашу профессию", reply_markup=kb_game)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
