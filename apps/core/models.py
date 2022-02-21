from django.db import models
from django.contrib.auth.models import User
from .validations import ValidationOnlyDay


class MonthYear(models.IntegerChoices):
    JAN = 1, "Janeiro"
    FEB = 2, "Fevereiro"
    MAR = 3, "Março"
    APR = 4, "Abril"
    MAY = 5, "Maio"
    JUN = 6, "Junho"
    JUL = 7, "Julho"
    AUG = 8, "Agosto"
    SEP = 9, "Setembro"
    OCT = 10, "Outubro"
    NOV = 11, "Novembro"
    DEC = 12, "Dezembro"


class Employee(models.Model):
    user = models.OneToOneField(on_delete=models.deletion.CASCADE, to=User)
    id_sheet_original = models.IntegerField(default=0, verbose_name="Id Planilha Original")
    department = models.CharField(max_length=20, verbose_name="Departamento")


class Planilha(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.deletion.CASCADE, verbose_name="Empregado")
    month = models.IntegerField(
        choices=MonthYear.choices,
        verbose_name="Mês")

    def __process_schedule(self):
        invalids = self.schedule_set.filter(lambda sch: not len(sch.hour_set) % 2)
        for invalid in invalids:
            invalid.invalid = True
            invalid.save()

    @property
    def total_schedule(self):
        self.__process_schedule()
        return self.schedule_set.filter(invalido=False).aggregate(models.Sum('balance'))['balance__sum'] or 0


class Schedule(models.Model):
    sheet = models.ForeignKey(Planilha, on_delete=models.deletion.CASCADE, verbose_name="Planilha")
    day = models.IntegerField(null=False, blank=False, validators=[ValidationOnlyDay()], verbose_name="Dia")
    invalid = models.BooleanField(default=False, verbose_name="É invalido")

    @property
    def balance(self):
        return self.hour_set.aggregate(models.Sum('hour'))['hour__sum'] or 0


class Hour(models.Model):
    hour = models.TimeField(default=0, verbose_name="Hora")
    schedule = models.ForeignKey(Schedule, on_delete=models.deletion.CASCADE, verbose_name="Planilha")


