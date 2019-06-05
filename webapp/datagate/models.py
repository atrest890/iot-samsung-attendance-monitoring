from django.db import models

from website.models import Building, Auditorium

class Device(models.Model):
    identifier = models.CharField(max_length = 32, unique = True)
    # building = models.ForeignKey(Building, on_delete = models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete = models.CASCADE)


class Log(models.Model):
    identifier_devices = models.CharField(max_length = 32, unique = True)
    identifier_card = models.CharField(max_length = 32, default = "0de8ddf24fd4424e2a0d29a21de4880e")
    date = models.DateField()