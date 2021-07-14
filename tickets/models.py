from django.db import models

# Create your models here.
from django.db import models

class Movie(models.Model):
    GENRE_CHOICES = (
        ('action', '動作片'),
        ('romance', '愛情片'),
        ('drama', '劇情片'),
    )
    title = models.CharField(max_length=100)  # 電影名稱
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)  # 電影類型
    release_year = models.IntegerField()  # 年份