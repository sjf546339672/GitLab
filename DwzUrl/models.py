from django.db import models

# Create your models here.


class ShortURLModel(models.Model):
    # 短url
    short_url = models.CharField(max_length=255)
    # 原始url
    long_url = models.CharField(max_length=255)


