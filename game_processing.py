#  game processing
from session import load_json, dump_json


def _load():
    pass


def _dump(data):
    pass


def set_main_message(session, user_id, message_id):
    data = load_json()
    user = data[session]["users"][str(user_id)]
    user["active_message_id"] = message_id

    dump_json(data)


def set_balance(session, user_id, message_id):
    data = load_json()
    user = data[session]["users"][str(user_id)]
    user["balance"] = user["income"]["salary"] + user["assets"]["saving"]
    user["balance_message_id"] = message_id
    dump_json(data)

    return user["balance"]


def edit_balance(session, user_id, price):
    data = load_json()
    user = data[session]["users"][str(user_id)]
    user["balance"] += price

    dump_json(data)
    return user["balance"]
    pass


def generate_user_card(session, user_id):
    data = load_json()
    user = data[session]["users"][user_id]
    card = ""
    card += "недвижимость: \n"
    user_active: dict = user["income"]["passive_income"]
    passive = 0
    for k, v in user_active.items():
        card += f"{k}: {v} \n"
        passive += v

    children = user["expenses"]["child_count"]
    card += f"\n кол-во детей: {children}\n\n"

    card += "акции: \n"
    actions: dict = user["assets"]["stocks"]
    for k, v in actions.values():
        card += f"{k}: {v} \n"

    ex: dict = user["expenses"]
    minus = ex["texes"] + ex["mortgage_house"] + ex["study"] + ex["car"] + ex["credit_card"] + ex["another"] + ex[
        "bank_credit_pay_price"] + ex["child_price"] * ex["child_count"]

    card += "\n"
    _sum = user["income"]["salary"] + passive - minus
    _s = f'{user["income"]["salary"]} + {passive} - {minus} = {_sum}'
    card += _s + "\n"
    card += f"Месячный денежный поток: {_sum}"
    return card


def start_game():
    pass


def generate_professionals():
    pass


def pay_day():
    pass


def add_gold_coin():
    pass


def sell_gold_coin():
    pass


def all_sorts_of_things():
    pass


def child():
    pass


def change_professional():
    pass


def actual_statistic():
    ...


def get_credit():
    pass


def pay_credit():
    pass


def bye_house():
    pass


def sell_house():
    pass


def bye_stock():
    pass


def sell_stock():
    pass
