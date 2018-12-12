from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name='events'
urlpatterns = [
    path('event/<int:pk>', views.event, name= 'event'),
    path('upload/', views.eventUpload, name='eventUpload'),
    path('eventlive/<int:pk>', views.eventlive, name= 'eventlive'),
    path('eventblock/<int:pk>', views.eventblock, name= 'eventblock'),
    path('admin/',views.admindashevents, name= 'admindashevents'),
    path('admin/pending/',views.pendingevent, name= 'pendingevent'),
    path('admin/new/',views.newevent, name= 'newevent'),
]
