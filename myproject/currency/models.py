from django.db import models


class CurrencyRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Время запроса
    usd_to_rub_rate = models.FloatField()                # Курс доллара к рублю

    def __str__(self):
        return f"{self.timestamp}: USD to RUB rate is {self.usd_to_rub_rate}"
