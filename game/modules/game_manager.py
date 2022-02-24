# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 15:08
# @Author  : Jinyi Li
# @FileName: game_manager.py
# @Software: PyCharm
from game.data import data
from game.modules import game_process
from game.models import Record
import pickle


class Manager:
    _instance = None
    data = None

    # As for singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.data = data

    def random_attribute(self, request_data, game=None):
        print("info: random attribute")
        user_id = request_data.get("user_id")
        if game is None:
            game = self.data.get_cache(user_id)

            if game is None:
                game = game_process.Process()

        game.random_attribute()
        data.set_cache(user_id, game)
        return game.role.attribute

    def initial_game(self, request_data, game):
        print("info: initial_game")
        attribute = self.random_attribute(request_data.get("user_id"), game)
        return attribute

    def start_game(self, request_data):
        print("info: start_game")
        game = self.data.get_cache(request_data.get("user_id"))
        game.role.first_name = request_data.get("first_name")
        game.role.last_name = request_data.get("last_name")
        game.role.head_portrait = request_data.get("head_portrait")
        return game.next()

    def serialize(self, request_data):
        user_id = request_data.get("user_id")
        p_stream = pickle.dumps(self.data.get_cache(user_id))
        return self.data.create(Record, user_id=user_id, data=p_stream)
