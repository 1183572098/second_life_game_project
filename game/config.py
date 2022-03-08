# -*- coding: UTF-8 -*-
import csv
import os


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


attribute = Attribute()


class Event(Config):

    def __init__(self):
        self.file_name = 'event.csv'
        super(Event, self).__init__()

    def get_event(self, age, event_history):
        event_list = {}
        for para in self.config:
            age_group = para["age group"]
            age_min, age_max = age_group.split(",")
            if (int(age_min) == -1 or age > int(age_min)) and (int(age_max) == -1 or age < int(age_max)):
                if int(para["EventType"]) == 0 and (int(para["pre_event"]) is None or int(para["pre_event"]) in event_history):
                    event_list.update({int(para["event ID"]): int(para["probability"])})

        return event_list

    def get_high_event(self, age, event_history, attributes):
        event_list = {}
        for para in self.config:
            age_group = para["age group"]
            age_min, age_max = age_group.split(",")
            if (int(age_min) == -1 or age > int(age_min)) and (int(age_max) == -1 or age < int(age_max)):
                if int(para["EventType"]) == 1 and (int(para["pre_event"]) is None or int(para["pre_event"]) in event_history):
                    if int(para["maximum"]) > attributes[int(para["attribute threshold"])] > int(para["minimum"]):
                        event_list.update({int(para["event ID"]): int(para["probability"])})

        return event_list

    def get_effect(self, event_id):
        effect_dict = {}
        for para in self.config:
            if para["event ID"] == event_id:
                if para["effect"] is not None:
                    effects = para["effect"].split(",")
                    for effect in effects:
                        attribute_id, value = effect.split(":")
                        effect_dict.update({int(attribute_id): int(value)})

                return effect_dict


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
