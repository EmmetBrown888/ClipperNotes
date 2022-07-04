from django.db import models


class OneTimeInfo(models.Model):
    text = models.TextField(verbose_name="Текст Записки")
    password = models.CharField(blank=True, null=True, max_length=200, verbose_name="Пароль")

    class Meta:
        verbose_name = 'Записка'
        verbose_name_plural = 'Записки'

    def __str__(self):
        return str(self.pk)


class CryptoWallet(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название валюты")
    wallet = models.CharField(max_length=200, verbose_name="Кошелек")

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'

    def __str__(self):
        return str(self.pk)
