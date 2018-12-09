from django.db import models
from django_unixdatetimefield import UnixDateTimeField
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to = 'images/', default = 'images/profile_pic.png')
    venue = models.CharField(max_length=128)
    date = UnixDateTimeField()
    associatedClub = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    isLive = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
