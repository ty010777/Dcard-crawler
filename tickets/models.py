from django.db import models
from django.db.models.fields import URLField
# Create your models here.


class CrawledData(models.Model):
    num = models.CharField(max_length=50,default='')
    cTitle = models.CharField(max_length=100,default='')
    cForumAlias = models.CharField(max_length=20,default='')
    cForumName = models.CharField(max_length=20,default='')
    cCommentCount = models.IntegerField(default=0)
    cLikeCount = models.IntegerField(default=0)
    cExcerpt = models.TextField(max_length=20,default='')
    cContent = models.TextField(max_length=800,default='')
    cTag = models.CharField(max_length=100,default='')
    mood=models.CharField(max_length=20,default='')
    link = models.URLField(max_length=200,default='')
    img = models.URLField(default='https://i.imgur.com/Ewmac29.jpg')

    class Meta:
        ordering = ['-cLikeCount']


# python manage.py makemigrations
# python manage.py migrate