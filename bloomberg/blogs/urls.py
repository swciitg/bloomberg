from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name='blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/',views.admindash, name= 'admindash'),
    path('admin/pending/',views.pendingpost, name= 'pendingpost'),
    path('admin/new/',views.newpost, name= 'newpost'),
    path('user/',views.userdash, name='userdash'),
    path('blog/<int:pk>', views.blog, name= 'blog'),
    path('upload/', views.blogUpload, name='blogUpload'),
    path('bloglive/<int:pk>', views.bloglive, name= 'bloglive'),
    path('blogblock/<int:pk>', views.blogblock, name= 'blogblock'),
]
