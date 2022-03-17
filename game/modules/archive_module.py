# -*- coding: utf-8 -*-
# @Time    : 2022/3/16 14:06
# @Author  : Jinyi Li
# @FileName: archive_module.py
# @Software: PyCharm
import pickle

from game.data import data
from game.models import Record
from game.modules import game_manager


def enter_archive(request):
    print("info:enter_archive")
    result = {}
    user_id = request.user.id
    manager = game_manager.Manager()
    if manager.has_game(user_id):
        result.update({"state": 1})
    else:
        result.update({"state": 0})

    records = data.select(Record.objects.get, Record, user_id=user_id)
    if records is None:
        result.update({"archive1": "null"})
        result.update({"archive2": "null"})
        result.update({"archive3": "null"})
    else:
        for record in records:
            game = pickle.loads(record.data)
            nickname = game.role.first_name + " " + game.role.last_name
            portrait = game.role.head_portrait
            age = game.role.age
            print(game.event_history)
            last_event = game.event_history[-1]
            save_time = record.time
            location = record.location
            result_key = "archive" + str(location)
            result_body = {"nickname": nickname,
                           "portrait": portrait,
                           "age": age,
                           "event": last_event,
                           "time": save_time}
            result.update({result_key: result_body})

    return result
