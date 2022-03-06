# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 15:03
# @Author  : Jinyi Li
# @FileName: game_process.py
# @Software: PyCharm
import random

from game.config import attribute, parameter, store_table


class Process:
    role = None
    bag = {}
    __consumed_bag = {}
    event_history = []

    def __init__(self):
        self.role = Role()

    def random_attribute(self):
        random_numbers = [random.random() for _ in range(len(self.role.attribute))]
        random_sum = sum(random_numbers)
        random_attributes = [int(value/random_sum*parameter.value(2001)) for value in random_numbers]
        if sum(random_attributes) != 100:
            random_attributes[-1] += 1
        index = 0
        for key in self.role.attribute.keys():
            self.role.set_attribute(key, random_attributes[index])
            index += 1

    def next_year(self):
        self.role.age += 1
        event_id = self._get_event(self.role.age)
        self.event_history.append(event_id)
        return {self.role.age: event_id}

    def _get_event(self, age):
        pass

    def _execute_event(self, event_id):
        pass

    def get_bag(self):
        return self.bag

    def get_shop(self):
        shop = store_table.get_goods()
        for k, v in self.bag:
            if shop.get(k) != -1:
                shop.update(k, shop.get(k)-v)

        for k, v in self.__consumed_bag:
            if shop.get(k) != -1:
                shop.update(k, shop.get(k)-v)

        return shop

    def purchase(self, good_id):
        if self.bag.get(good_id) is None:
            self.bag.update({good_id: 1})
        else:
            self.bag.update({good_id: self.bag.get(good_id) + 1})

    def use_good(self, good_id):
        if self.bag.get(good_id) == 1:
            del self.bag[good_id]
        else:
            self.bag.update({good_id: self.bag.get(good_id) - 1})

        self._use_good(good_id)
        if self.__consumed_bag.get(good_id) is None:
            self.__consumed_bag.update({good_id: 1})
        else:
            self.bag.update({good_id: self.__consumed_bag.get(good_id) + 1})

    def _use_good(self, good_id):
        good_type = store_table.get_type(good_id)
        if good_type == 0:
            for k, v in store_table.get_type(good_id):
                if v != 0:
                    attribute_id = int(k[5:])
                    self.role.set_attribute(attribute_id, self.role.get_attribute(attribute_id) + v)

        elif good_type == 1:
            event_id = store_table.get_event(good_id)
            self._execute_event(event_id)

        else:
            print("error: unknown type of good")


class Role:
    attribute = {}
    first_name = None
    last_name = None
    head_portrait = None
    age = None

    def __init__(self):
        for attribute_id in attribute.ids():
            self.attribute.update({attribute_id: 0})
        self.age = -1  # unborn

    def get_attribute(self, attribute_id):
        return self.attribute.get(attribute_id)

    def set_attribute(self, attribute_id, value):
        return self.attribute.update({attribute_id: value})
