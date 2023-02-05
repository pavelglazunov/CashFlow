import random
import json


def load_json():
    with open("sessions.json", mode="r", encoding="utf-8") as file:
        return json.load(file)


def dump_json(data):
    with open("sessions.json", encoding="utf-8", mode="w") as f:
        json.dump(data, f)


def check_user_active_game(user_id):
    all_sessions = load_json()

    for users in all_sessions:
        if str(user_id) in all_sessions[users]["users"]:
            return "Вы уже принимаете участие в другой игре"


def get_session_players(token):
    return load_json()[token]["users"]


def create_session(user_id, user_token):
    all_sessions = load_json()

    for users in all_sessions.values():
        if user_id in users["users"]:
            return "Вы уже принимаете участие в другой игре"

    if not (user_token in all_sessions):
        all_sessions[user_token] = {"metadata": {"game_status": 0, "game_player_count": 1, "admin": user_id},
                                    "users": {
                                        str(user_id): {
                                            "profession": None,
                                            "expenses": None,  # без детей м крилитов
                                            "children_expenses": None,
                                            "saving": None,

                                            "salary": None,
                                            "real_estate": {},
                                            "children_count": 0,
                                            "stocks": {},
                                            "credits": {},

                                        }
                                    }}

        dump_json(all_sessions)
        return ""

    return "Данный токен уже занят, пожалуйста, придуиайте другой"


def join_session(token, user_id):
    all_sessions = load_json()

    for users in all_sessions.values():
        if user_id in users["users"]:
            return "Вы уже принимаете участие в другой игре"

    if token in all_sessions:
        if all_sessions[token]["metadata"]["game_player_count"] <= 5:
            all_sessions[token]["metadata"]["game_player_count"] += 1
            all_sessions[token]["users"][str(user_id)] = {
                "profession": None,
                "expenses": None,  # без детей м крилитов
                "children_expenses": None,
                "saving": None,

                "salary": None,
                "real_estate": {},
                "children_count": 0,
                "stocks": {},
                "credits": {},

            }

            dump_json(all_sessions)
            return ""
        return "В данной игре нет мест"
    return "Некоректный токен, пожалуйста проверьте его"


def exit_from_session(user_id):
    all_sessions = load_json()

    for session in all_sessions:
        if str(user_id) in all_sessions[session]["users"]:
            all_sessions[session]["users"].pop(str(user_id))
            all_sessions[session]["metadata"]["game_player_count"] -= 1

            dump_json(all_sessions)
            return ["Вы успешно вышли из игры", session]
    return ["Вы еще не находитесь ни в одной игре", None]


def remove_session(token, user_id):
    all_sessions = load_json()

    if (token in all_sessions) and (all_sessions[token]["metadata"]["admin"] == user_id):
        users = all_sessions[token]["users"].keys()

        all_sessions.pop(token)

        dump_json(all_sessions)

        return ["", users]

    return ["Вы не являетесь админом игры или игры с таким токеном несуществует, "
            "повторите попытку или введите 0 для отмены", []]


def get_session_by_admin(user_id):
    all_sessions = load_json()

    for i in all_sessions:
        if all_sessions[i]["metadata"]["admin"] == user_id:
            return [i, all_sessions[i]["users"].keys()]
    return False
