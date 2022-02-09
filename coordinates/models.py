from django.db import models




class Coordinates(models.Model):
    address = models.CharField('адрес места', max_length=30, unique=True)
    lat = models.FloatField(verbose_name='Широта', blank=True, null=True)
    lon = models.FloatField(verbose_name='Долгота', blank=True, null=True)
    launch_geocoder_date = models.DateTimeField(
        'Дата запроса к геокодеру',
        unique=True,
    )

    class Meta:
        verbose_name = 'адрес доставки'
        verbose_name_plural = 'адреса доставки'

    def __str__(self):
        return self.address