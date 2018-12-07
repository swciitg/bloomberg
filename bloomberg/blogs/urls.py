from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('blogs/', views.index, name='index'),
    path('', RedirectView.as_view(url='/blogs/')),
    path('login/', views.login, name= 'login'),
    path('signup/' , views.signup , name = 'signup'),
    path('blogs/admin/',views.admindash, name= 'admindash'),
    path('blogs/admin/pending/',views.pendingpost, name= 'pendingpost'),
    path('blogs/admin/new/',views.newpost, name= 'newpost'),
    path('blogs/user/',views.userdash, name='userdash'),
    path('logout/', views.logout, name= 'logout'),
    path('blogs/blog/<int:pk>', views.blog, name= 'blog'),
    path('blogs/permissiondenied/', views.permissiondenied, name= 'permissiondenied'),
    path('blogs/upload/', views.blogUpload, name='blogUpload'),
    path('blogs/bloglive/<int:pk>', views.bloglive, name= 'bloglive'),
    path('blogs/blogblock/<int:pk>', views.blogblock, name= 'blogblock'),
]
