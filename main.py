import random

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from forms import StartGame, JoinGame, RemoveGame, Professionals, UserAnswer, DealData
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


@dp.message_handler(state=UserAnswer.vv_answer)
async def get_answer(message: types.Message, state: FSMContext):
    price = message.text
    user = get_user_data(UserAnswer.__session_name__, message.from_user.id)
    session = UserAnswer.__session_name__

    child_kb = InlineKeyboardMarkup(resize=True)
    child_kb.insert(InlineKeyboardButton("С условием на детей", callback_data=f"@ch=T;{session};{price}"))
    child_kb.insert(InlineKeyboardButton("Без условия на детей", callback_data=f"@ch=F;{session};{price}"))

    await bot.edit_message_text(f"Сумма вычета: {price}", message.chat.id, user["active_message_id"],
                                reply_markup=child_kb)
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()


small_deal = {}


@dp.message_handler(state=DealData.answer1)
async def get_answer1(message: types.Message, state: FSMContext):
    if message.text == "мелкая сделка":
        small_deal["type"] = "small"
        await bot.edit_message_text("Уажите необходимую сделку", message.chat.id, DealData.__message__,
                                    reply_markup=kb_deal_l2)
        await DealData.next()


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
    kb_game_menu.insert(InlineKeyboardButton("✴️ день выплат ✴️", callback_data=f"#pd;{session}"))
    kb_game_menu.row(InlineKeyboardButton("🆘 всякая всячина 🆘", callback_data=f"#vv;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("✅ сделка ✅", callback_data=f"#dl;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🌐 рынок 🌐", callback_data=f"#mk;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🚺 благотворительность 🚺", callback_data=f"#ct;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🚹 ребенок 🚹", callback_data=f"#cl;{session}"))
    kb_game_menu.insert(InlineKeyboardButton("🛂 увольнение 🛂", callback_data=f"#dm;{session}"))

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


@dp.callback_query_handler(Text(startswith="#"))
async def game_processing_handler(callback: types.CallbackQuery):
    """ #pd - день выплат
        #vv - всякая всячина
        #dl - сделка
        #mk - рынок
        #ct - благотворительность
        #cl - ребенок
        #dm - увольнение
"""
    type_, session = callback.data.split(";")
    user_id = callback.from_user.id
    user = get_user_data(session, user_id)

    if type_ == "#pd":
        balance = edit_balance(session, user_id, get_month_cash_flow(session, user_id))
        if user["have_bonus"]:
            balance += 500 if random.randint(1, 6) > 3 else 0
        await bot.edit_message_text(f"Текущий баланс: {balance}", callback.message.chat.id, user["balance_message_id"])
    if type_ == "#vv":
        await bot.edit_message_text("Введите сумму вычета: ", callback.message.chat.id, user["active_message_id"])
        UserAnswer.__session_name__ = session
        await UserAnswer.vv_answer.set()
    if type_ == "#ct":
        balance = edit_balance(session, user_id, -get_month_cash_flow(session, user_id) * 0.1)
        await bot.edit_message_text(f"Текущий баланс: {balance}", callback.message.chat.id, user["balance_message_id"])
    if type_ == "#cl":
        user_children = user["expenses"]["child_count"]
        if user_children < 3:
            add_child(session, user_id)
            card = generate_user_card(session, user_id)
            await bot.edit_message_text(card, callback.message.chat.id, user["active_message_id"],
                                        reply_markup=kb_game_menu(session))
    if type_ == "#dm":
        ex: dict = user["expenses"]
        minus = ex["texes"] + ex["mortgage_house"] + ex["study"] + ex["car"] + ex["credit_card"] + ex["another"] + ex[
            "bank_credit_pay_price"] + ex["child_price"] * ex["child_count"]

        balance = edit_balance(session, user_id, -minus)
        await bot.edit_message_text(f"Текущий баланс: {balance}", callback.message.chat.id, user["balance_message_id"])

    if type_ == "#dl":
        await bot.edit_message_text("Уажите тип сделки", callback.message.chat.id, user["active_message_id"],
                                    reply_markup=kb_deal)
        DealData.__session_name__ = session
        DealData.__user_id__ = user_id
        DealData.__message__ = user["active_message_id"]
        await DealData.answer1.set()


@dp.callback_query_handler(Text(startswith="@"))
async def param_handler(callback: types.CallbackQuery):
    type_, session, get_data = callback.data.split(";")
    user_id = callback.from_user.id
    user = get_user_data(session, user_id)

    if (type_ == "@ch=T" and not user["expenses"]["child_count"]) or (type_ == "@ch=F"):
        price = int(get_data)
        if price >= 1800 and user["balance"] < price:
            delta = price - user["balance"]
            credit_price = [i for i in range(delta, delta + 1001) if i % 1000 == 0][0]
            get_credit(session, user_id, credit_price)
        balance = edit_balance(session, user_id, -price)

    await bot.edit_message_text(f"Текущий баланс: {balance}", callback.message.chat.id, user["balance_message_id"])
    card = generate_user_card(session, user_id)

    await bot.edit_message_text(card, callback.message.chat.id, user["active_message_id"],
                                reply_markup=kb_game_menu(session))


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

            for i in session["users"]:
                print(session)
                kb_professional = InlineKeyboardMarkup(resize_keyboard=True)

                print(i)
                for k in PROFESSIONALS_LIST_RU:
                    kb_professional.add(
                        InlineKeyboardButton(k, callback_data=f"prof={k};{session['metadata']['session_name']};{i}")
                    )
                await bot.send_message(i, "Начало игры, укажите вашу профессию", reply_markup=kb_professional)
                await Professionals.prof.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
