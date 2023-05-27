import pytz
import requests
from django.core.exceptions import ValidationError
import re
from django.db import models


class Distribution(models.Model):
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    start_date = models.DateTimeField()
    text = models.TextField()
    tag = models.CharField(max_length=255)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.text


class Client(models.Model):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    phone_number = models.CharField(max_length=11)
    mobile_operator = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=50)

    def clean(self):
        super().clean()
        if not re.match(r'^7\d{10}$', self.phone_number):
            raise ValidationError('Некорректный номер телефона. Номер должен быть в формате 7xxxxxxxxxx')

        try:
            pytz.timezone(self.time_zone)
        except pytz.UnknownTimeZoneError:
            raise ValidationError('Некорректный часовой пояс')

    def __str__(self):
        return self.phone_number


class Message(models.Model):
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    creation_date = models.DateTimeField()
    status = models.BooleanField()
    distribution = models.ForeignKey(Distribution, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.creation_date)

