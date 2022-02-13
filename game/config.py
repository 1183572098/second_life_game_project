import csv
import os
from itertools import islice


class SystemConfig(object):
    parameter = {}

    def __init__(self):
        work_path = os.path.dirname(os.path.abspath(__file__))
        print(work_path)
        csv_reader = csv.reader(open(os.path.join(work_path, '../static/config/parameter.csv')))
        for line in islice(csv_reader, 1, None):
            self.parameter.update({int(line[0]): line[1]})


system_config = SystemConfig()
