import json
import os.path

SHEET_HORARIO = 1



class ProcessadorXLS2Dict:
    def __init__(self, file_name):
        self.builder = None
        # self.file_name = file_name
        self.file_name = os.path.abspath("amostras/JULHO 2021.XLS")

    def build(self):
        import pandas as p
        # nome_planilha = p.ExcelFile(self.file_name).sheet_names[SHEET_HORARIO]
        # excel = p.read_excel(self.file_name, nome_planilha)
        excel = p.read_excel(self.file_name, SHEET_HORARIO)
        excel = excel.replace('\\n', ' ')
        self.builder = json.loads(excel)
        return self

    def get_dict(self):
        if self.builder:
            return self.builder
        else:
            raise Exception("Not build yet.")

    def process(self):

        pass

    def __str__(self):
        return json.dumps(self.builder) if not self.builder else ""


if __name__ == '__main__':
    processador = ProcessadorXLS2Dict('')
    processador.builder()
    jerson = processador.get_dict()
    print(jerson)


