import csv
import os
from itertools import islice


class Parameter(object):
    parameter = []

    def __init__(self):
        work_path = os.path.dirname(os.path.abspath(__file__))
        parameter_file = csv.DictReader(open(os.path.join(work_path, '../static/config/parameter.csv')))
        for role in parameter_file:
            self.parameter.append(dict(role))

    def value(self, parameter_id):
        for para in self.parameter:
            if para["id"] == str(parameter_id):
                return int(para["value"])

        raise Exception("Can't find parameter id: " + str(parameter_id))


parameter = Parameter()
