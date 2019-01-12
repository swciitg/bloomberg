from django.db import models
from django_unixdatetimefield import UnixDateTimeField
from django.contrib.staticfiles.templatetags.staticfiles import static


# Create your models here.
class Blog(models.Model):
    blogID = models.CharField(max_length=11)
    title = models.CharField(max_length=128)
    authorID = models.CharField(max_length=7)
    name = models.CharField(max_length=50)
    isLive = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    tags =  models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'images/', default = 'images/325505.jpg')
    lastUpdated = UnixDateTimeField(auto_now=True)
    createdAt = UnixDateTimeField(auto_now_add=True)
    content = models.TextField()
    approvedBy = models.CharField(max_length=50 , null = True , blank = True)
    topic = models.CharField(max_length=100)

    class Meta:
        ordering = ['-createdAt']

    def __str__(self):
        return self.title

class Comment(models.Model):
    commentID = models.CharField(max_length=17)
    blogID = models.CharField(max_length=11)
    author = models.CharField(max_length = 7)
    isLive = models.BooleanField(default = False)
    content = models.TextField(max_length = 1000)
