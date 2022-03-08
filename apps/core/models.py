import datetime

from django.db import models
from django.contrib.auth.models import User
# from .validations import ValidationOnlyDay


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

    @staticmethod
    def get_by_int(val):
        rtn = list(item for item in MonthYear.__members__.values() if item.value == val)
        if not rtn: # Quando estiver vazio adicionar None
            rtn.append(None)
        return rtn.pop()


class Employee(models.Model):
    user = models.OneToOneField(on_delete=models.deletion.CASCADE, to=User)
    id_sheet_original = models.IntegerField(default=0, unique=True, verbose_name="Id Planilha Original")
    department = models.CharField(max_length=20, verbose_name="Departamento")

    def __str__(self):
        return "{} - {} - {}".format(self.user.username, self.id_sheet_original, self.department)


class Sheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.deletion.CASCADE, verbose_name="Empregado")
    month = models.IntegerField(
        choices=MonthYear.choices,
        verbose_name="Mês")

    def __str__(self):
        return self.get_month_display()

    def __process_schedule(self):
        for invalid in self.schedule_set.all():
            if invalid.hour_set.count() % 2 and not invalid.invalid:
                invalid.invalid = True
                invalid.save()

    @property
    def has_invalid_schedule(self):
        return self.schedule_set.contains(invalid=True)

    @property
    def total_schedule(self):
        self.__process_schedule()
        total = 0
        for hour in self.schedule_set.all().filter(invalid=False).all():
            total += hour.balance
        return total


class Schedule(models.Model):
    sheet = models.ForeignKey(Sheet, on_delete=models.deletion.CASCADE, verbose_name="Planilha")
    day = models.IntegerField(null=False, blank=False,
                              # validators=[ValidationOnlyDay(sheet.month)],
                              verbose_name="Dia")
    invalid = models.BooleanField(default=False, verbose_name="É invalido")

    def __str__(self):
        return "{} - {}".format(self.day, self.invalid)
    @property
    def balance(self):
        entrada = 0
        saida = 0
        for idx, hour in enumerate(self.hour_set.all()):
            if idx % 2:
                saida += hour.hour_datetime.timestamp()
            else:
                entrada += hour.hour_datetime.timestamp()
        return saida - entrada


class Hour(models.Model):
    _MASK_HOUR = "%H:%M"
    hour = models.CharField(max_length=5, default="0", null=False, verbose_name="Hora")
    schedule = models.ForeignKey(Schedule, on_delete=models.deletion.CASCADE, verbose_name="Planilha")

    @property
    def hour_datetime(self):
        return datetime.datetime.strptime(self.hour, self._MASK_HOUR)

    def __str__(self):
        return self.hour_datetime
