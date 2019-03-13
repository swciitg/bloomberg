from django.contrib import admin
from .models import Question, Choice, Question_exit_poll, Candidate
# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Question_exit_poll)
admin.site.register(Candidate)
