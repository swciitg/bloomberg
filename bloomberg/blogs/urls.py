from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name= 'login'),
    path('signup/' , views.signup , name = 'signup'),
    path('admin/',views.admindash, name= 'admindash'),
    path('admin/pending/',views.pendingpost, name= 'pendingpost'),
    path('admin/new/',views.newpost, name= 'newpost'),
    path('user/',views.userdash, name='userdash'),
    path('logout/', views.logout, name= 'logout'),
    path('blog/<int:pk>', views.blog, name= 'blog'),
    path('permissiondenied/', views.permissiondenied, name= 'permissiondenied'),
    path('upload/', views.blogUpload, name='blogUpload'),
    path('bloglive/<int:pk>', views.bloglive, name= 'bloglive'),
    path('blogblock/<int:pk>', views.blogblock, name= 'blogblock'),
]
