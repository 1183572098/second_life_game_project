# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 15:03
# @Author  : Jinyi Li
# @FileName: game_process.py
# @Software: PyCharm
import random

from game.config import attribute, parameter


class Process:
    role = None
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


class Role:
    attribute = {}
    first_name = None
    last_name = None
    head_portrait = None

    def __init__(self):
        for attribute_id in attribute.ids():
            self.attribute.update({attribute_id: 0})

    def get_attribute(self, attribute_id):
        return self.attribute.get(attribute_id)

    def set_attribute(self, attribute_id, value):
        return self.attribute.update({attribute_id: value})
