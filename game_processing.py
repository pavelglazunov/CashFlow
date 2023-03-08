#  game processing
from session import load_json, dump_json


def _load():
    pass


def _dump(data):
    pass


def get_month_cash_flow(session, user_id):
    data = load_json()
    user = data[session]["users"][str(user_id)]
    passive_income = sum([v for v in user["income"]["passive_income"].values()])
    expenses = sum([user["expenses"][i] for i in
                    ["texes", "mortgage_house", "study", "car", "credit_card", "another", "bank_credit_pay_price"]])
    expenses += user["expenses"]["child_price"] * user["expenses"]["child_count"]
    month_cash_flow = user["income"]["salary"] + passive_income - expenses

    return month_cash_flow


def set_main_message(session, user_id, message_id):
    data = load_json()
    user = data[session]["users"][str(user_id)]
    user["active_message_id"] = message_id

    dump_json(data)


def set_balance(session, user_id, message_id):
    data = load_json()
    user = data[session]["users"][str(user_id)]
    user["balance"] = get_month_cash_flow(session, user_id) + user["assets"]["saving"]
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
    user = data[session]["users"][str(user_id)]
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


def get_credit(session, user_id, price):
    data = load_json()
    user = data[session]["users"][str(user_id)]
    user["liabilities"]["bank_credit"] += price
    user["expenses"]["bank_credit_pay_price"] = user["liabilities"]["bank_credit"] * 0.1
    user["balance"] += price

    dump_json(data)


def add_child(session, user_id):
    data = load_json()

    user = data[session]["users"][str(user_id)]
    user["expenses"]["child_count"] += 1

    dump_json(data)