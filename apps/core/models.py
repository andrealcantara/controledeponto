from django.db import models

# Create your models here.


class Funcionario(models.Model):
    user = models.OneToOneField(on_delete=models.constraints.)
    nome
    id_planilha
    departamento
    horarios[]



    def total_horario(self):
        count = 0
        for horario in self.horarios:
            for


class Horario(models.Model):
    dia
    registros[]