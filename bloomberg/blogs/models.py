from django.db import models
from django_unixdatetimefield import UnixDateTimeField
from django.contrib.staticfiles.templatetags.staticfiles import static


# Create your models here.
class UserDetail(models.Model):
    userID = models.CharField(max_length=7)
    name = models.CharField(max_length = 50)
    emailID = models.EmailField(max_length = 50)
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to = 'images/', default = 'images/profile_pic.png')
    mobile = models.IntegerField()
    totalBlogsWritten = models.IntegerField(default=0)
    isBlocked = models.BooleanField(default = False)
    isAdmin = models.BooleanField(default = False)
    isModerator = models.BooleanField(default = False)


    def __str__(self):
        return self.name

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
    approvedBy = models.CharField(max_length=7 , null = True , blank = True)
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

class Session(models.Model):
    userID = models.CharField(max_length=7)
    name = models.CharField(max_length = 50)
    emailID = models.EmailField(max_length = 50)
    logInTime = UnixDateTimeField()
    logOutTime = UnixDateTimeField()
    isExpired = models.BooleanField(default = False)

    def __str__(self):
        return self.name
