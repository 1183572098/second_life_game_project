# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 15:03
# @Author  : Jinyi Li
# @FileName: game_process.py
# @Software: PyCharm
import random

from game.config import attribute, parameter, store_table, option_config, event, option_table


class Process:
    role = None
    bag = {}
    __consumed_bag = {}
    event_history = []
    initial_attribute = None

    def __init__(self):
        self.role = Role()
        self.initial_attribute = self.role.attribute

    def random_attribute(self):
        random_numbers = [random.random() for _ in range(len(self.role.attribute))]
        random_sum = sum(random_numbers)
        random_attributes = [int(value/random_sum*parameter.value(2001)) for value in random_numbers]
        if sum(random_attributes) != int(parameter.value(2001)):
            random_attributes[-1] += int(parameter.value(2001)) - sum(random_attributes)
        index = 0
        for key in self.role.attribute.keys():
            self.role.set_attribute(key, random_attributes[index])
            index += 1

    def next_year(self):
        is_end = self.end
        result = {}
        if is_end > 0:
            self.role.age += 1
            self.mechanism_process()
            event_id = self._get_event()
            self._execute_event(event_id)
            result.update({"is_end": False})
            result.update({self.role.age: event_id})
            result.update({"event_id": event_id})
            result.update({"attribute": self.role.attribute})
        else:
            result.update({"is_end": True})
            result.update({"attribute_id": is_end})

        return result

    @property
    def end(self):
        for k, v in self.role.attribute.items():
            if v <= 0:
                return k

        return -1

    def mechanism_process(self):
        if parameter.value(2005) > self.role.age > parameter.value(2004):
            effect_str = parameter.str_value(2006)
        elif self.role.age > parameter.value(2005):
            effect_str = parameter.str_value(2007)
        else:
            return

        effects = effect_str.split(",")
        for e in effects:
            e, p = e.split(":")
            self.role.set_attribute(int(e), self.role.get_attribute(int(e)) + int(p))

    def _get_event(self):
        if self.role.age in option_config.ages():
            event_dict = option_config.get_event(self.role.age)
        else:
            event_dict = event.get_high_event(self.role.age, self.event_history, self.role.attribute)
            if len(event_dict) == 0:
                event_dict = event.get_event(self.role.age, self.event_history, self.role.attribute)

        if len(event_dict) == 1:
            return event_dict.keys()[0]
        else:
            return self._get_random_by_weights(event_dict)

    def _get_random_by_weights(self, obj_dict):
        sum_weights = sum(obj_dict.values())
        random_num = random.random()
        weight = 0
        for k, v in obj_dict:
            weight += v
            if weight / sum_weights * 1.0 >= random_num:
                return k

    def _execute_event(self, event_id):
        if event_id == 3001:
            self.rebirth()
            return

        self.event_history.append(event_id)
        effect_dict = event.get_effect(event_id)
        for k, v in effect_dict:
            self.role.set_attribute(k, self.role.get_attribute(k) + v)

    def rebirth(self):
        self.role.age = 0
        self.role.attribute = self.initial_attribute
        self.event_history.clear()
        self.event_history.append(3001)

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
            for k, v in store_table.get_values(good_id):
                if v != 0:
                    self.role.set_attribute(k, self.role.get_attribute(k) + v)

        elif good_type == 1:
            event_id = store_table.get_event(good_id)
            self._execute_event(event_id)

        elif good_type == 2:
            weight_dict = store_table.get_weight(good_id)
            attribute_id = self._get_random_by_weights(weight_dict)
            self.role.set_attribute(attribute_id, self.role.get_attribute(attribute_id) + store_table.get_values(good_id)[attribute_id])

        else:
            print("error: unknown type of good")

    def choose_option(self, option_id):
        event_id = option_table.get_event(self.event_history[-1], option_id)
        result = {}
        self._execute_event(event_id)
        result.update({"event_id": event_id})
        result.update({"attribute": self.role.attribute})
        return result


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
