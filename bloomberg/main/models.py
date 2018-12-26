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

class Session(models.Model):
    userID = models.CharField(max_length=7)
    name = models.CharField(max_length = 50)
    emailID = models.EmailField(max_length = 50)
    logInTime = UnixDateTimeField(null=True , blank=True)
    logOutTime = UnixDateTimeField(null=True , blank=False)
    isExpired = models.BooleanField(default = False)

    def __str__(self):
        return self.name
