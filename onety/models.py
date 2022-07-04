from django.db import models


class OnetyModel(models.Model):
    text = models.TextField(verbose_name="Текст Записки")
    email = models.CharField(blank=True, null=True, max_length=200, verbose_name="Email уведомление")

    class Meta:
        verbose_name = 'Записка'
        verbose_name_plural = 'Записки'

    def __str__(self):
        return str(self.pk)
