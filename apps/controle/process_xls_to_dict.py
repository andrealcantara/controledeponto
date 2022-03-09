import copy
import json
import os
import pandas as p

from django.contrib.auth.models import User
from apps.core.models import Employee, Sheet, MonthYear, Schedule, Hour
from apps.core import constants



class ProcessadorXLS2Dict:
    """
        Classe que mantem e processa o XLS e passa para Dict
    """

    def __init__(self, file_name):
        self._builder = {}
        self._file_name = file_name

    def _build(self, number_sheet=constants.SHEET_HORARIO) -> None:
        sheet = {constants.SOURCE: p.read_excel(self._file_name, number_sheet)}
        sheet[constants.SOURCE].replace(os.linesep, " ")
        _excel_to_json = sheet[constants.SOURCE].to_json()
        sheet[constants.STRUCTURE] = json.loads(_excel_to_json)
        self._builder[number_sheet] = sheet

    def sz_columns_rows(self, number_sheet=constants.SHEET_HORARIO) -> [int, int]:
        back = []
        if number_sheet not in self._builder:
            self._build(number_sheet)
        if not self._builder[number_sheet][constants.SOURCE].empty:
            back = list(self._builder[number_sheet][constants.SOURCE].shape)
        return back

    def get_dict(self, number_sheet=constants.SHEET_HORARIO) -> dict:
        ret = {}
        if number_sheet not in self._builder:
            self._build(number_sheet)

        if self._builder[number_sheet][constants.STRUCTURE]:
            ret = copy.deepcopy(self._builder[number_sheet][constants.STRUCTURE])

        return ret

    def __str__(self, number_sheet=constants.SHEET_HORARIO):
        if number_sheet not in self._builder:
            self._build(number_sheet)

        if self._builder[number_sheet][constants.STRUCTURE]:
            return str(self._builder[number_sheet][constants.STRUCTURE])
        return str({})


class ProcessadorDict2Object:
    def __init__(self, process: ProcessadorXLS2Dict):
        if process is None:
            raise BaseException("Process can't be None")
        self._process = process

    def _parse_to_structure_employee(self, number_sheet=constants.SHEET_HORARIO) -> list:
        _dict = self._process.get_dict(number_sheet)
        sz = self._process.sz_columns_rows(number_sheet)
        sz[0] -= constants.SIZE_HEADER
        keys = _dict.keys()
        employees = []
        for key in keys:
            count_employee = 0
            for idx in range(0, sz[0], constants.SIZE_ROWS_EMPOYLE):
                if len(employees) > count_employee:
                    employee = employees[count_employee]
                else:
                    employee = _create_employee()
                    employees.append(employee)
                _populate_employee(_dict, employee, idx, key)
                count_employee += 1
        _identify_employees(employees)
        return employees

    def get_object(self, number_sheet=constants.SHEET_HORARIO):
        employees_dict = self._parse_to_structure_employee(number_sheet)
        employees = []
        for row in employees_dict:
            user = User.objects.get_or_create(username=row[constants.LABEL_NAME])[0]
            employee = Employee.objects.get_or_create(user=user, id_sheet_original=row[constants.LABEL_ID],
                                                      department=row[constants.LABEL_DEPARTMENT])[0]
            employees.append(employee)
            sheet = Sheet.objects.get_or_create(employee=employee, month=MonthYear.get_by_int(self.get_month()))[0]
            for i in range(len(row[constants.LABEL_HOUR])):
                schedule = Schedule.objects.get_or_create(sheet=sheet, sheet_id=sheet.id,
                                                          day=int(row[constants.LABEL_DAYS][i]))[0]
                if row[constants.LABEL_HOUR][i]:
                    hours = row[constants.LABEL_HOUR][i].strip().split(os.linesep)
                    for hour in (x for x in hours if not x.isspace()):
                        Hour.objects.create(schedule=schedule, hour=hour[:5])
                else:
                    Hour.objects.create(schedule=schedule)
        pass

    def get_month(self, number_sheet=constants.SHEET_HORARIO):
        _DICT = self._process.get_dict(number_sheet)
        _LINE = list(_DICT.keys())[2]  # 2 é a 3th linha que vai ter a informação
        _COLUMN = list(_DICT[_LINE].keys())[1]  # 1 é a 2nd coluna que vai ter a informacao
        return int(_DICT[_LINE][_COLUMN].split(" ")[0].split("/")[1])


def _populate_employee(dic, employee, idx, key):
    idx += constants.SIZE_HEADER
    employee[constants.LABEL_DAYS].append(int(dic[key][str(idx)]))

    idx += 1
    employee[constants.LABEL_DATA].append(dic[key][str(idx)])

    idx += 1
    employee[constants.LABEL_HOUR].append(dic[key][str(idx)])


def _create_employee():
    return {
        constants.LABEL_DATA: [],
        constants.LABEL_DAYS: [],
        constants.LABEL_HOUR: []
    }


def _identify_employees(employees):
    _INDEX_ID = 2
    _INDEX_NAME = 10
    _INDEX_DEPARTMENT = 20
    for val in employees:
        val[constants.LABEL_ID] = val[constants.LABEL_DATA][_INDEX_ID]
        val[constants.LABEL_NAME] = val[constants.LABEL_DATA][_INDEX_NAME]
        val[constants.LABEL_DEPARTMENT] = val[constants.LABEL_DATA][_INDEX_DEPARTMENT]
