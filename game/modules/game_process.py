# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 15:03
# @Author  : Jinyi Li
# @FileName: game_process.py
# @Software: PyCharm
import random

from game.config import attribute, parameter, store_table, option_config, event, option_table, state_table


class Process:

    def __init__(self):
        self.bag = {}
        self.__consumed_bag = {}
        self.event_history = []
        self.initial_attribute = None
        self.shop = None
        self.role = Role()
        self.shop = store_table.get_goods()

    def random_attribute(self):
        random_attributes = []
        attribute_num = len(self.role.attribute)
        available_value = int(parameter.value(2001))
        for i in range(attribute_num - 1):
            random_num = random.randint(int(parameter.value(2002)), min([int(parameter.value(2003)), available_value - (attribute_num - i - 1) * int(parameter.value(2002))]))

            available_value -= random_num
            random_attributes.append(random_num)

        random_attributes.append(available_value)
        index = 0
        for key in self.role.attribute.keys():
            self.role.set_attribute(key, random_attributes[index])
            index += 1

    def next_year(self):
        if self.initial_attribute is None:
            self.initial_attribute = self.role.attribute.copy()

        is_end = self.end
        result = {}
        if is_end < 0:
            self.role.age += 1
            self.mechanism_process()
            event_id = self._get_event()
            if str(event_id)[0] == "2":
                self.rebirth(event_id)
            if str(event_id)[0] == "3":
                self._execute_event(event_id)
            else:
                self.event_history.append(event_id)

            result.update({"is_end": 0})
            result.update({"age": self.role.age})
            result.update({"event_id": event_id})
            result.update({"attribute": self.role.visible_attribute})
        else:
            result.update({"is_end": 1})
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
        for ef in effects:
            e, p = ef.split(":")
            self.role.set_attribute(int(e), self.role.get_attribute(int(e)) + int(p))

    def _get_event(self):
        if self.role.age in option_config.ages():
            event_dict = option_config.get_event(self.role)
            event_dict = option_table.filter(event_dict, self.role, self.event_history)
            if len(event_dict) == 0:
                event_dict = event.get_event(self.role, self.event_history)

        else:
            event_dict = event.get_event(self.role, self.event_history)

        if len(event_dict) == 1:
            return list(event_dict.keys())[0]
        else:
            return self._get_random_by_weights(event_dict)

    def _get_random_by_weights(self, obj_dict):
        sum_weights = sum(obj_dict.values())
        random_num = random.random()
        weight = 0
        for k, v in obj_dict.items():
            weight += v
            if weight / sum_weights * 1.0 >= random_num:
                return k

    def _execute_event(self, event_id):
        if event.get_after_state(event_id) is not None:
            self._change_state(event.get_after_state(event_id))

        self.event_history.append(event_id)
        effect_dict = event.get_effect(event_id)
        if effect_dict is not None:
            for k, v in effect_dict.items():
                self.role.set_attribute(k, self.role.get_attribute(k) + v)

    def _change_state(self, state_list):
        for state in state_list:
            exclusive_states = state_table.get_exclusive_state(state)
            if exclusive_states is not None:
                for exclusive_state in exclusive_states:
                    if exclusive_state in self.role.state:
                        self.role.state.remove(exclusive_state)

            self.role.state.append(state)

    def rebirth(self, event_id):
        self.role.age = 0
        self.role.attribute = self.initial_attribute
        self.role.state.clear()
        self.event_history.clear()
        self.event_history.append(event_id)
        self._change_state(event.get_after_state(event_id))

    def get_bag(self):
        return self.bag

    def get_shop(self):
        return self.shop

    def _update_shop(self, shop, bag_dict):
        for k, v in bag_dict.items():
            if shop.get(k) != -1:
                if shop.get(k)-v == 0:
                    del shop[k]
                else:
                    shop.update({k: shop.get(k)-v})
        return shop

    def purchase(self, good_id):
        money_dict = store_table.get_money(good_id)
        for k, v in money_dict.items():
            if self.role.attribute.get(k) < v:
                return False
            else:
                self.role.attribute.update({k, self.role.attribute.get(k) - v})

        if self.bag.get(good_id) is None:
            self.bag.update({good_id: 1})
        else:
            self.bag.update({good_id: self.bag.get(good_id) + 1})

        if self.shop.get(good_id) != -1:
            if self.shop.get(good_id) != 1:
                self.shop.update({good_id: self.shop.get(good_id) - 1})
            else:
                del self.shop[good_id]
        return True

    def use_good(self, good_id):
        if self.bag.get(good_id) == 1:
            del self.bag[good_id]
        else:
            self.bag.update({good_id: self.bag.get(good_id) - 1})

        self._use_good(good_id)
        if self.__consumed_bag.get(good_id) is None:
            self.__consumed_bag.update({good_id: 1})
        else:
            self.__consumed_bag.update({good_id: self.__consumed_bag.get(good_id) + 1})

    def _use_good(self, good_id):
        good_type = store_table.get_type(good_id)
        if good_type == 0:
            for k, v in store_table.get_values(good_id).items():
                if v != 0:
                    self.role.set_attribute(k, self.role.get_attribute(k) + v)

        elif good_type == 1:
            event_id = store_table.get_event(good_id)
            self._execute_event(event_id)

        elif good_type == 2:
            weight_dict = store_table.get_weight(good_id)
            attribute_id = self._get_random_by_weights(weight_dict)
            self.role.set_attribute(attribute_id, self.role.get_attribute(attribute_id) + store_table.get_values(good_id)[attribute_id])
        elif good_type == 3:
            weight_dict = store_table.get_weight(good_id)
            for i in range(2):
                attribute_id = self._get_random_by_weights(weight_dict)
                self.role.set_attribute(attribute_id, self.role.get_attribute(attribute_id) + store_table.get_range_values(good_id, i)[attribute_id])

        else:
            print("error: unknown type of good")

    def choose_option(self, option_id):
        event_id = option_table.get_event(self.event_history[-1], option_id)
        result = {}
        self._execute_event(event_id)
        result.update({"event_id": event_id})
        result.update({"attribute": self.role.visible_attribute})
        return result


class Role:

    def __init__(self):
        self.attribute = {}
        self.first_name = None
        self.last_name = None
        self.head_portrait = None
        self.age = None
        for attribute_id in attribute.ids():
            self.attribute.update({attribute_id: 0})
        self.age = -1  # unborn
        self.state = []

    def get_attribute(self, attribute_id):
        return self.attribute.get(attribute_id)

    def set_attribute(self, attribute_id, value):
        return self.attribute.update({int(attribute_id): value})

    @property
    def visible_attribute(self):
        visible_attribute = {}
        for k, v in self.attribute.items():
            if attribute.visible(k):
                visible_attribute.update({k: v})

        return visible_attribute
