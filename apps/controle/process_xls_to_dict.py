import copy
import json

import pandas as p
from django.contrib.auth.models import User

from apps.core.models import Employee, Sheet, MonthYear

_SHEET_HORARIO = 1
_SIZE_HEADER = 2
_SIZE_ROWS_EMPOYLE = 3


class ProcessadorXLS2Dict:
    """
        Classe que mantem e processa o XLS e passa para Dict
    """

    def __init__(self, file_name):
        self._builder = {}
        self._file_name = file_name

    def _build(self, number_sheet=_SHEET_HORARIO):

        sheet = {"excel": p.read_excel(self._file_name, number_sheet)}
        sheet["excel"].replace("\\n", " ")
        _excel_to_json = sheet["excel"].to_json()
        sheet["dict"] = json.loads(_excel_to_json)
        self._builder[number_sheet] = sheet

    def sz_columns_rows(self, number_sheet=_SHEET_HORARIO) -> [int, int]:
        back = []
        if number_sheet not in self._builder:
            self._build(number_sheet)

        if not self._builder[number_sheet]["excel"].empty:
            back = list(self._builder[number_sheet]["excel"].shape)
        return back

    def get_dict(self, number_sheet=_SHEET_HORARIO) -> dict:
        ret = {}

        if number_sheet not in self._builder:
            self._build(number_sheet)

        if self._builder[number_sheet]["dict"]:
            ret = copy.deepcopy(self._builder[number_sheet]["dict"])

        return ret

    def __str__(self, number_sheet=_SHEET_HORARIO):
        if number_sheet not in self._builder:
            self._build(number_sheet)

        if self._builder[number_sheet]["dict"]:
            return str(self._builder[number_sheet]["dict"])
        return str({})


class ProcessadorDict2Object:
    def __init__(self, process: ProcessadorXLS2Dict):
        if process is None:
            raise BaseException("Process can't be None")
        self._process = process

    def _parse_to_structure_employee(self) -> list:
        _dict = self._process.get_dict()
        sz = self._process.sz_columns_rows()
        sz[0] -= _SIZE_HEADER
        keys = _dict.keys()
        employees = []
        for key in keys:
            count_employee = 0
            for idx in range(0, sz[0], _SIZE_ROWS_EMPOYLE):
                if len(employees) > count_employee:
                    employee = employees[count_employee]
                else:
                    employee = _create_employee()
                    employees.append(employee)
                _populate_employee(_dict, employee, idx, key)
                count_employee += 1
        _identify_employees(employees)
        return employees

    def get_object(self, sheet_number=_SHEET_HORARIO):
        employees = self._parse_to_structure_employee()
        for row in employees:
            user = User.objects.get_or_create(username=row["name"])[0]
            employee = Employee.objects.get_or_create(user=user, id_sheet_original=row["id"],
                                                      department=row["department"])[0]
            sheet = Sheet.objects.get_or_create(employee=employee, month=MonthYear.get_by_int(self.get_month()))



        pass

    def get_month(self):
        _dict = self._process.get_dict()
        _LINE = list(_dict.keys())[2]  # 2 é a 3th linha que vai ter a informação
        _COLUMN = list(_dict[_LINE].keys())[1]  # 1 é a 2nd coluna que vai ter a informacao
        return int(_dict[_LINE][_COLUMN].split(" ")[0].split("/")[1])


def _populate_employee(dic, employee, idx, key):
    idx += _SIZE_HEADER
    employee["days"].append(int(dic[key][str(idx)]))

    idx += 1
    employee["data"].append(dic[key][str(idx)])

    idx += 1
    employee["hours"].append(dic[key][str(idx)])


def _create_employee():
    return {
        "data": [],
        "days": [],
        "hours": []
    }


def _identify_employees(employees):
    for val in employees:
        val["id"] = val["data"][2]
        val["name"] = val["data"][10]
        val["department"] = val["data"][20]
