from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name='main'

urlpatterns = [
    path('', views.index, name= 'index'),
    path('about_us/',views.about, name='about'),
    path('login/', views.login, name= 'login'),
    path('signup/' , views.signup , name = 'signup'),
    path('logout/', views.logout, name= 'logout'),
    path('permissiondenied/', views.permissiondenied, name= 'permissiondenied'),
]
