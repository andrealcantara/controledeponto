import copy
import json

import pandas as p

from apps.core.models import Employee

SHEET_HORARIO = 1


class ProcessadorXLS2Dict:
    """
        Classe que mantem e processa o XLS e passa para Dict
    """

    def __init__(self, file_name):
        self.__builder = None
        self.__excel = None
        self.__file_name = file_name

    def build(self):
        self.__excel = p.read_excel(self.__file_name, SHEET_HORARIO)
        self.__excel.replace("\\n", " ")
        jason = self.__excel.to_json()
        self.__builder = json.loads(jason)

    def sz_columns_rows(self):
        return self.__excel.shape

    def get_dict(self):
        if self.__builder:
            ret = copy.deepcopy(self.__builder)
            return ret
        else:
            raise AttributeError("Not build yet.")

    def __str__(self):
        if self.__builder is not None:
            return self.get_dict()
        return {}


class ProcessadorDict2Object:
    def __init__(self, process: ProcessadorXLS2Dict):
        try:
            if process is None:
                raise BaseException("Process can't be None")
            process.get_dict()
        except AttributeError as e:
            process.build()
        self.__proc = process


    def parse_to_Employee(self):
        sz = self.__proc.sz_columns_rows()
        sz[0] -= 2
        num_empoyler = sz[0] / 3
