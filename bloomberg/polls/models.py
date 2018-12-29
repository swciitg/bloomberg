from django.db import models
from django_unixdatetimefield import UnixDateTimeField
# Create your models here.

class individual_survey_exit_poll(models.Model):
    access_code = models.CharField(max_length = 50)
    candidate_for_VP = models.CharField(max_length = 50)
    candidate_for_techboardGS = models.CharField(max_length = 50)
    candidate_for_welfareboardGS = models.CharField(max_length = 50)
    is_used = models.BooleanField(default=False)

class exit_poll_stats(models.Model):
    access_codes_used = models.IntegerField(default=0)
    candidate_for_vp_1 = models.IntegerField()
    candidate_for_vp_2 = models.IntegerField()
    candidate_for_techboardGS_1 = models.IntegerField()
    candidate_for_techboardGS_2 = models.IntegerField()
    candidate_for_welfareboardGS_1 = models.IntegerField()
    candidate_for_welfareboardGS_2 = models.IntegerField()
    is_active = models.BooleanField(default=True)

class individual_survey_pre_poll(models.Model):
    access_code = models.CharField(max_length = 50)
    candidate_for_VP = models.CharField(max_length = 50)
    candidate_for_techboardGS = models.CharField(max_length = 50)
    candidate_for_welfareboardGS = models.CharField(max_length = 50)
    is_used = models.BooleanField(default=False)

class pre_polls_stats(models.Model):
    access_codes_used = models.IntegerField(default=0)
    candidate_for_vp_1 = models.IntegerField()
    candidate_for_vp_2 = models.IntegerField()
    candidate_for_techboardGS_1 = models.IntegerField()
    candidate_for_techboardGS_2 = models.IntegerField()
    candidate_for_welfareboardGS_1 = models.IntegerField()
    candidate_for_welfareboardGS_2 = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    createdAt = UnixDateTimeField(auto_now_add=True)
    authorID = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    isLive = models.BooleanField(default=False)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
