# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 15:08
# @Author  : Jinyi Li
# @FileName: game_manager.py
# @Software: PyCharm
from game.data import data
from game.modules import game_process
from game.models import Record
import pickle
from game.config import parameter
import json


class Manager:
    _instance = None
    data = None
    player_games = {}

    # As for singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.data = data

    def random_attribute(self, request_data, game=None):
        print("info: random attribute")
        user_id = request_data.user.id
        if game is None:
            if user_id in self.player_games.keys():
                game = self.player_games[user_id]
            else:
                game = game_process.Process()

        game.random_attribute()

        self.player_games.update({user_id: game})
        result = {}
        result.update({"attribute": game.role.visible_attribute})
        return result

    def initial_game(self, request_data, game):
        print("info: initial_game")
        attribute = self.random_attribute(request_data, game)
        return attribute

    def start_game(self, request_data):
        print("info: start_game")
        game = self.player_games.get(request_data.user.id)
        game.role.first_name = request_data.POST.get("first_name")
        game.role.last_name = request_data.POST.get("last_name")
        result = {}
        if game.role.first_name is None or game.role.last_name is None:
            result.update({"success": 0})
            result.update({"reason": "Player's name should not be null"})
            return result

        game.role.head_portrait = request_data.POST.get("head_portrait")
        attributes = json.loads(request_data.POST.get("attribute"))

        for v in attributes.values():
            if v < parameter.value(2002) or v > parameter.value(2003):
                result.update({"success": 0})
                result.update({"reason": "The initial attribute cannot be lower than 10 and cannot be higher than 50"})
                return result

        for k, v in attributes.items():
            game.role.set_attribute(k, v)

        result.update({"success": 1})
        return result

    def enter_game(self, request_data):
        print("info: enter_game")
        game = self.player_games.get(request_data.user.id)
        if game is not None:
            result = game.next_year()
        else:
            result = None
        return result

    def open_shop(self, request_data):
        print("info: open_shop")
        game = self.player_games.get(request_data.user.id)
        bag = game.get_bag()
        shop = game.get_shop()

        result = {}
        result.update({"bag": bag})
        result.update({"shop": shop})
        return result

    def purchase(self, request_data):
        print("info: purchase")
        game = self.player_games.get(request_data.user.id)
        good_id = int(request_data.POST.get("good_id"))
        shop = game.get_shop()
        result = {}
        if shop.get(good_id) is None:
            print("error: can't purchase")
            result.update({"success": 0})
            result.update({"reason": "The good is not in the store"})
        if shop.get(good_id) == -1 or shop.get(good_id) > 0:
            success = game.purchase(good_id)
            if success:
                result.update({"success": 1})
                result.update({"attribute": game.role.visible_attribute})
                result.update(self.open_shop(request_data))
            else:
                result.update({"success": 0})
                result.update({"reason": "Attribute value is not enough"})
        else:
            print("info: can't purchase")
            result.update({"success": 0})
            result.update({"reason": "Insufficient number of the good available for purchase"})
            result.update({"attribute": game.role.visible_attribute})
        return result

    def use_good(self, request_data):
        print("info: use good")
        game = self.player_games.get(request_data.user.id)
        good_id = int(request_data.POST.get("good_id"))
        bag = game.get_bag()
        result = {}
        if bag.get(good_id) is not None:
            game.use_good(good_id)
            result.update({"success": 1})
            result.update({"age": game.role.age})
            result.update({"event_id": game.event_history[-1]})
            result.update({"attribute": game.role.visible_attribute})
            result.update(self.open_shop(request_data))
        else:
            print("error: can't purchase")
            result.update({"success": 0})
            result.update({"reason": "The good is not in the bag"})

        return result

    def choose_option(self, request_data):
        print("info: choose option")
        game = self.player_games.get(request_data.user.id)
        option_id = request_data.POST.get("option")[6:]
        return game.choose_option(option_id)

    def serialize(self, request_data):
        print("info: serialize")
        p_stream = pickle.dumps(self.player_games.get(request_data.user.id))
        loc = request_data.POST.get('location')
        record = self.data.select(Record.objects.get, Record, user_id=request_data.user.id, location=loc)
        result = {}
        if record is None:
            result_code = self.data.create(Record, user_id=request_data.user.id, data=p_stream, location=loc)
        else:
            result_code = self.data.update(record, data=p_stream)
        result.update({"success": 1 if result_code else 0})
        return result

    def deserialize(self, request_data):
        print("info: deserialize")
        loc = request_data.POST.get('location')
        record = self.data.select(Record.objects.get, Record, user_id=request_data.user.id, location=loc)
        result = {}
        if record is None:
            print("record is none")
            result.update({"success": 0})
            result.update({"reason": "Archive is not exist."})
            return result

        else:
            game = pickle.loads(record.data)
            self.player_games.update({request_data.user.id: game})
            result.update({"success": 1})
            return result

    def has_game(self, user_id):
        return user_id in self.player_games.keys()

    def reload_game(self, request_data):
        print("info: reload_game")
        user_id = request_data.user.id
        game = self.player_games.get(user_id)
        result = {}
        if game is None:
            print("error: game not exist.")
            result.update({"success": 0})
            result.update({"reason": "game is lost"})
            return result

        else:
            result.update({"success": 1})
            result.update({"is_end": game.end})
            result.update({"age": game.role.age})
            result.update({"event_id": game.event_history})
            result.update({"attribute": game.role.visible_attribute})

        return result

    def exit_game(self, request_data):
        user_id = request_data.user.id
        if user_id in self.player_games.keys():
            del self.player_games[user_id]
