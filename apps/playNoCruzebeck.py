import os

from apps.controle.process_xls_to_dict import ProcessadorXLS2Dict, ProcessadorDict2Object


def run():
    file_name = os.path.abspath("amostras/JUNHO 2021.XLS")
    processador = ProcessadorXLS2Dict(file_name)
    proc_empoyller = ProcessadorDict2Object(processador)
    employees = proc_empoyller._parse_to_structure_employee()
    proc_empoyller.get_object()
    print(proc_empoyller.get_month())
    print(employees)
    print((lambda x: x * 2)("\n"))
    print(processador)


if __name__ == '__main__':
    run()
