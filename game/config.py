import csv
import os


class Config(object):
    file_name = None

    def __init__(self):
        self.config = []
        work_path = os.path.dirname(os.path.abspath(__file__))
        parameter_file = csv.DictReader(open(os.path.join(work_path, '../static/config/' + self.file_name)))
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
