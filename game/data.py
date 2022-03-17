# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 16:24
# @Author  : Jinyi Li
# @FileName: data.py
# @Software: PyCharm

# This file provides a unified calling interface for the database and cache, reducing the coding complexity of the
# module when calling data

from django.core.cache import cache
import game.models as models
import inspect
from game.config import parameter


class DataProcess(object):
    _instance = None

    data_cache = cache
    classes = []

    # As for singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.__get_models()

    def __get_models(self):
        classes = inspect.getmembers(models, inspect.isclass)
        for (name, _) in classes:
            variables = [attr for attr in dir(_) if not callable(getattr(_, attr)) and not attr.startswith("_")]
            self.classes.append((_, name, variables))

        print("register models success.")

    def set_cache(self, key, value, timeout=parameter.value(1001)):
        """
        Update a key-value pair in the cache
        :param key: cache key
        :param value: cache value
        :param timeout: cache timeout
        :return: None
        """
        self.data_cache.set(key, value, timeout)

    def get_cache(self, key):
        """
        Get a value in the cache by the key
        :param key: cache key
        :return: cache value
        """
        if isinstance(key, str):
            if self.data_cache.has_key(key):
                return self.data_cache.get(key)
            else:
                return None

        elif isinstance(key, list):
            data_list = []
            for k in key:
                if self.data_cache.has_key(key):
                    data_list.append(self.data_cache.get(k))

            return data_list
        else:
            raise Exception("Input type of 'key' must be str or list.")

    # Just return 1 object
    def __select_key_from_all_models(self, key):
        model_list = []
        for obj, n, v in self.classes:
            if v.contains(key):
                model_list.append(obj)

        if len(model_list) > 1:
            raise Exception("The query field exists in multiple tables, please confirm the input or specify the object")

        return model_list[0]

    def __get_model_by_name(self, model):
        if type(model) == str:
            for obj, n, v in self.classes:
                if n == model:
                    return obj
        else:
            for obj, n, v in self.classes:
                if obj == model:
                    return obj

        raise Exception("Can't find such a model named: " + model)

    def model(self, name):
        """
        Get the model object of a certain name
        :param name: model name, type of str
        :return: model object, type of model
        """
        return self.__get_model_by_name(name)

    def select(self, select_func, tables, *args, **kwargs):
        """
        Query data from a database or cache. If the data exists in the cache, the data in the cache will be returned.
        If the data in the cache does not exist, the database query function will be executed and the query result
        will be returned.
        :param select_func: Query function, this is a callback function
        :param tables: Query function, which is a callback function. eg. Blog.objects.values_list
        :param args: non-keyword arguments. eg. 'id', 'name'
        :param kwargs: keyword arguments  eg. headline='Hello'
        :return: query result, data object
        """
        cache_key = self.__transform_to_cache_key(tables, *args, **kwargs)
        if self.data_cache.has_key(cache_key):
            print("Get data from cache")
            try:
                cache_data = self.data_cache.get(cache_key)
            except Exception as e:
                print(e)
                cache_data = None

            return cache_data
        else:
            print("Get data from database")
            try:
                result_data = select_func(*args, **kwargs)
                if not isinstance(result_data, list):
                    result_data = [result_data]
                self.data_cache.set(cache_key, result_data, parameter.value(1001))
            except Exception as e:
                print("no record exists.")
                result_data = None

            return result_data

    def __transform_to_cache_key(self, tables, *args, **kwargs):
        cache_key = ""
        if type(tables) != list:
            tables = [tables]

        for table in tables:
            for obj, n, v in self.classes:
                if table == obj or table == n:
                    cache_key += n

        for arg in args:
            cache_key += str(arg)

        for key in kwargs:
            cache_key += str(key) + str(kwargs[key])

        return cache_key

    def create(self, model, **kwargs):
        """
        Add a row of data
        :param model: Model object or model name, type of model or str
        :param kwargs: keyword arguments. eg. first_name="Bruce", last_name="Springsteen"
        :return: None
        """
        try:
            obj = self.__get_model_by_name(model)
            o = obj.objects.create(**kwargs)
            o.save()
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, data_objs, **kwargs):
        """
        Update one or more rows of data
        :param data_objs: data objects, type of model object or list of model objects
        :param kwargs: The data to be modified is passed as keyword arguments. eg. views=20
        :return: None
        """
        # Get the class name of the first object in the list, because the objects of a group of update operations
        # must be instances of the same class
        try:
            cache_head = data_objs[0].__class__.__name__
            self.__delete_cache(cache_head)
            for data_obj in data_objs:
                for key in kwargs:
                    setattr(data_obj, key, kwargs[key])
                data_obj.save()

            # Delayed double deletion
            self.__delete_cache(cache_head)
            return True
        except Exception as e:
            print(e)
            return False

    def __delete_cache(self, key_str):
        for key in self.data_cache.keys():
            if key_str in key:
                self.data_cache.delete(key)


data = DataProcess()
