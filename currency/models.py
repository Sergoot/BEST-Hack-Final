from django.db import models

# Create your models here.
from users.models import CustomUser


class Currency(models.Model):
    name = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True, default='')
    price = models.FloatField(default=1, null=True)

    def __str__(self):
        return self.name
