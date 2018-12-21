from django.db import models
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
