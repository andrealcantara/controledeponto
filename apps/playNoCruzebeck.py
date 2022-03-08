import os
import time

from apps.controle.process_xls_to_dict import ProcessadorXLS2Dict, ProcessadorDict2Object


def run():
    ts = time.time()
    file_name = os.path.abspath("amostras/JUNHO 2021.XLS")
    processador = ProcessadorXLS2Dict(file_name)
    proc_empoyller = ProcessadorDict2Object(processador)
    objs = proc_empoyller.get_object()
    print(objs)
    print(time.time() - ts)

if __name__ == '__main__':
    run()
