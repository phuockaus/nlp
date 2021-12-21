from abc import ABC
from functools import reduce


class Database(ABC):
    def __init__(self, file):
        super().__init__()
        f = open(file)
        raw_data = [row for row in f]
        raw_data_pp = list(
            map(lambda row: self.__preProcessing(row), raw_data))
        self.data = self.__gen(raw_data_pp)
        f.close()

    @staticmethod
    def __preProcessing(string):
        data = string[1:-2]
        data = data.split(' ')
        return data

    @staticmethod
    def __gen(raw_data_pp):
        train_list = [data[1] for data in raw_data_pp if data[0] == 'TRAIN']
        atime_list = [data[1:] for data in raw_data_pp if data[0] == 'ATIME']
        dtime_list = [data[1:] for data in raw_data_pp if data[0] == 'DTIME']
        runtime_list = [data[1:]
                        for data in raw_data_pp if data[0] == 'RUN-TIME']
        return {'train_list': train_list, 'atime_list': atime_list, 'dtime_list': dtime_list, 'runtime_list': runtime_list}

    def getData(self):
        return self.data
