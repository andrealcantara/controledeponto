import os

from apps.controle.process_xls_to_dict import ProcessadorXLS2Dict, ProcessadorDict2Object

if __name__ == '__main__':
    file_name = os.path.abspath("../amostras/JUNHO 2021.XLS")
    processador = ProcessadorXLS2Dict(file_name)
    processador.build()
    proc_empoyller = ProcessadorDict2Object(processador)
    empoyllers = proc_empoyller.parse_to_Employee()

    print(processador.sz_columns_rows())
