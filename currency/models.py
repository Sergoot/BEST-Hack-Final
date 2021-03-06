from django.db import models

# Create your models here.
from users.models import CustomUser


class Currency(models.Model):
    name = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True, default='')
    price = models.FloatField(default=1, null=True)
    ru_title = models.CharField(max_length=50,default='')

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default='')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, default='')
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0, null=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='стоимость', default=0, null=True)

