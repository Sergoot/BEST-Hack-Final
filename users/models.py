from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as l
from django.db import models
# Create your models here.


class CustomUser(AbstractUser):

    username = models.CharField(max_length=16, unique=True)

    rub = models.DecimalField(max_digits=15, decimal_places=4, null=True, default=0)
    dollar = models.DecimalField(max_digits=15, decimal_places=4, null=True, default=0)
    euro = models.DecimalField(max_digits=15, decimal_places=4, null=True, default=0)
    yen = models.DecimalField(max_digits=15, decimal_places=4, null=True, default=0)
    frank = models.DecimalField(max_digits=15, decimal_places=4, null=True, default=0)
    hryvnia = models.DecimalField(max_digits=15, decimal_places=4, null=True, default=0)

    def __str__(self):
        return self.username


