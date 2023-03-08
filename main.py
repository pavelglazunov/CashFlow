from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from forms import StartGame, JoinGame, RemoveGame, Professionals
from functions import validate_token
from kb import *
from session import create_session, join_session, check_user_active_game, get_session_players, exit_from_session, \
    remove_session, get_session_by_admin, get_user_data, load_json, dump_json
from game_processing import *
from professional import PROFESSIONALS_LIST_EN, PROFESSIONALS_LIST_RU

from bt import TOKEN

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в CashFlow bot, укажите необходимое действие", reply_markup=kb_start)


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
    await message.answer("Некорректный токен, введите другой")
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


@dp.callback_query_handler(Text(startswith="prof="))
async def set_user_professional(callback: types.CallbackQuery):
    data = load_json()

    session = callback.data.split(";")[1]
    user_id = callback.data.split(";")[2]

    data[session]["users"][user_id] = PROFESSIONALS_LIST_EN[
        PROFESSIONALS_LIST_RU.index(callback.data.split(";")[0].split("=")[1])]

    dump_json(data)

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    msg = await bot.send_message(callback.message.chat.id, "Текущий баланс: ")

    balance = set_balance(callback.data.split(";")[1], callback.from_user.id, msg["message_id"])

    await bot.edit_message_text(f"Текущий баланс: {balance}", callback.message.chat.id, msg["message_id"])
    # await bot.pin_chat_message(callback.message.chat.id, msg["message_id"], disable_notification=False)

    kb_game_menu = InlineKeyboardMarkup(row_width=3)
    kb_game_menu.insert(InlineKeyboardButton("✴️ день выплат ✴️", callback_data=f"#pd;{user_id}"))
    kb_game_menu.row(InlineKeyboardButton("🆘 всякая всячина 🆘", callback_data=f"#vv;{user_id}"))
    kb_game_menu.insert(InlineKeyboardButton("✅ сделка ✅", callback_data=f"#dl;{user_id}"))
    kb_game_menu.insert(InlineKeyboardButton("🌐 рынок 🌐", callback_data=f"#mk;{user_id}"))
    kb_game_menu.insert(InlineKeyboardButton("🚺 благотворительность 🚺", callback_data=f"#ct;{user_id}"))
    kb_game_menu.insert(InlineKeyboardButton("🚹 ребенок 🚹", callback_data=f"#cl;{user_id}"))
    kb_game_menu.insert(InlineKeyboardButton("🛂 увольнение 🛂", callback_data=f"#dm;{user_id}"))

    card = generate_user_card(session, user_id)
    main_message = await bot.send_message(callback.message.chat.id, card,
                                          reply_markup=kb_game_menu)
    main_message_id = main_message["message_id"]

    set_main_message(session, user_id, main_message_id)

    # print(callback.data)
    # print(user_id, session_name, user_id)
    # print(user_professional)

    # user = get_user_data("amogus", user_id)
    pass


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
            # print(session)
            if session["metadata"]["game_player_count"] < 2:
                await message.answer("Недостаточное количество игроков")
                return

            start_game()

            for i in session["users"]:
                print(session)
                kb_professional = InlineKeyboardMarkup(resize_keyboard=True)

                print(i)
                for k in PROFESSIONALS_LIST_RU:
                    print(k)
                    kb_professional.add(
                        InlineKeyboardButton(k, callback_data=f"prof={k};{session['metadata']['session_name']};{i}")
                    )
                await bot.send_message(i, "Начало игры, укажите вашу профессию", reply_markup=kb_professional)
                await Professionals.prof.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
