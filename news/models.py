from django.db import models


class New(models.Model):
    title = models.CharField(max_length=64)


class Category(models.Model):
    title = models.CharField(max_length=255)
    new = models.ForeignKey(New, on_delete=models.CASCADE, null=True, blank=True)
    short = models.CharField(max_length=50, default='')
    ru_title = models.CharField(max_length=255, default=title)

    def __str__(self):
        return self.title


