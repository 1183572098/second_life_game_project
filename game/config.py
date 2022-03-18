# -*- coding: UTF-8 -*-
import csv
import os


def modify_ternary_expression(expression_str):
    formula, results = expression_str.split("?")
    option1, option2 = results.split(":")
    return option1 + " if " + formula + " else " + option2


class Config(object):
    file_name = None

    def __init__(self):
        self.config = []
        work_path = os.path.dirname(os.path.abspath(__file__))
        parameter_file = csv.DictReader(open(os.path.join(work_path, '../static/config/' + self.file_name), encoding="utf-8-sig"))
        for role in parameter_file:
            self.config.append(dict(role))


class Parameter(Config):

    def __init__(self):
        self.file_name = 'parameter.csv'
        super(Parameter, self).__init__()

    def value(self, parameter_id):
        for para in self.config:
            if para["id"] == str(parameter_id):
                return int(para["value"])

        raise Exception("Can't find parameter id: " + str(parameter_id))

    def str_value(self, parameter_id):
        for para in self.config:
            if para["id"] == str(parameter_id):
                return para["value"]

        raise Exception("Can't find parameter id: " + str(parameter_id))


parameter = Parameter()


class Attribute(Config):
    id_list = []

    def __init__(self):
        self.file_name = 'attribute.csv'
        super(Attribute, self).__init__()

    def ids(self):
        if not self.id_list:
            for para in self.config:
                self.id_list.append(int(para["attribute_id"]))

        return self.id_list

    def name(self, attribute_id):
        for para in self.config:
            if para["attribute_id"] == str(attribute_id):
                return para["attribute_name"]

    def visible(self, parameter_id):
        for para in self.config:
            if para["attribute_id"] == str(parameter_id):
                return int(para["is_hidden"]) == 0


attribute = Attribute()


class Event(Config):

    def __init__(self):
        self.file_name = 'event.csv'
        super(Event, self).__init__()

    def get_event(self, role, event_history):
        event_list = {}
        for k, v in role.attribute.items():
            exec('{} = {}'.format(attribute.name(k), v))

        for para in self.config:
            age_group = para["age group"]
            age_min, age_max = age_group.split(",")
            if int(para["EventType"]) == 0 or (int(para["EventType"]) == 1 and (int(para["maximum"]) > role.attribute[int(para["attribute threshold"])] >= int(para["minimum"]))):
                if (int(age_min) == -1 or role.age >= int(age_min)) and (int(age_max) == -1 or role.age <= int(age_max)):
                    if (para["pre_event"] == "" or self._satisfy_pre(para["pre_event"].split(","), event_history)) and (para["exclusive_events"] == "" or self._satisfy_exclusive(para["exclusive_events"].split(","), event_history)):
                        if int(para["IsRepeated"]) == 1 or int(para["event ID"]) not in event_history:
                            pre_state_list = para["pre_state_id"].split(",")
                            is_ready = True
                            if pre_state_list[0] != "":
                                for pre_state in pre_state_list:
                                    if pre_state not in role.state:
                                        is_ready = False
                                        break

                            if is_ready:
                                try:
                                    weight = int(para["probability"])
                                except Exception as e:
                                    weight = eval(modify_ternary_expression(para["probability"]))
                                event_list.update({int(para["event ID"]): weight})

        return event_list

    def _satisfy_pre(self, pre_events, event_history):
        for pre_events in pre_events:
            if int(pre_events) in event_history:
                continue
            return False
        return True

    def _satisfy_exclusive(self, exclusive_events, event_history):
        for exclusive_event in exclusive_events:
            if int(exclusive_event) in event_history:
                return False
        return True

    def get_effect(self, event_id):
        effect_dict = {}
        for para in self.config:
            if para["event ID"] == str(event_id):
                if para["effect"] != "":
                    effects = para["effect"].split(",")
                    for effect in effects:
                        attribute_id, value = effect.split(":")
                        effect_dict.update({int(attribute_id): int(value)})

                return effect_dict

    def get_after_state(self, event_id):
        for para in self.config:
            if para["event ID"] == str(event_id):
                if para["after_state_id"] == "":
                    return None
                else:
                    after_state_ids = para["after_state_id"].split(",")
                    return after_state_ids


event = Event()


class StoreTable(Config):
    goods = {}

    def __init__(self):
        self.file_name = 'StoreTable.csv'
        super(StoreTable, self).__init__()

    def get_goods(self):
        if not self.goods:
            for para in self.config:
                self.goods.update({int(para["ID"]): int(para["num"])})

        return self.goods.copy()

    def get_type(self, good_id):
        for para in self.config:
            if para["ID"] == str(good_id):
                return int(para["Type"])

    def get_values(self, good_id):
        values = {}
        for para in self.config:
            if para["ID"] == str(good_id):
                values.update({1: int(para["value1"]),
                               2: int(para["value2"]),
                               3: int(para["value3"]),
                               4: int(para["value4"]),
                               5: int(para["value5"])})

        return values

    def get_event(self, good_id):
        for para in self.config:
            if para["ID"] == str(good_id):
                return int(para["event trigger ID"])

    def get_weight(self, good_id):
        weight_dict = {}
        for para in self.config:
            if para["ID"] == str(good_id):
                weights = para["Weight"].split(",")
                i = 1
                for weight in weights:
                    weight_dict.update({i: int(weight)})
                    i += 1

        return weight_dict


store_table = StoreTable()


class OptionConfig(Config):
    age_list = []

    def __init__(self):
        self.file_name = 'OptionConfig.csv'
        super(OptionConfig, self).__init__()

    def ages(self):
        if not self.age_list:
            for para in self.config:
                self.age_list.append(int(para["age"]))

        return self.age_list

    def get_event(self, age):
        for para in self.config:
            if para["age"] == str(age):
                events = para["event_id"].split(",")
                event_dict = {}
                for e in events:
                    e, p = e.split(":")
                    event_dict.update({int(e): int(p)})
                return event_dict

        return None


option_config = OptionConfig()


class OptionTable(Config):

    def __init__(self):
        self.file_name = 'OptionTable.csv'
        super(OptionTable, self).__init__()

    def get_event(self, event_id, option_id):
        for para in self.config:
            if para["event_id"] == str(event_id):
                return int(para["event" + str(option_id)])


option_table = OptionTable()


class StateTable(Config):

    def __init__(self):
        self.file_name = 'StateTable.csv'
        super(StateTable, self).__init__()

    def get_exclusive_state(self, state_id):
        exclusive_state_list = []
        for para in self.config:
            if para["state_id"] == str(state_id):
                if para["exclusive_state_id"] != "":
                    exclusive_state_list = para["exclusive_state_id"].split(",")

                return exclusive_state_list


state_table = StateTable()
