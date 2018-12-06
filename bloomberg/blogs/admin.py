from django.contrib import admin
from .models import UserDetail , Blog , Comment, Session

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Session)
