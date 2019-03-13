from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
	path('<int:question_id>/vote/', views.vote, name='vote'),
	path('<int:question_id>/exitpollvote/', views.exitpollvote, name='exitpollvote'),
	path('upload/',views.polladdform, name='polladdform'),
	path('polllive/<int:pk>', views.polllive, name= 'polllive'),
    path('pollblock/<int:pk>', views.pollblock, name= 'pollblock'),
    path('admin/',views.admindashpolls, name= 'admindashpolls'),
    path('admin/pending/',views.pendingpolls, name= 'pendingpolls'),
    path('admin/new/',views.newpolls, name= 'newpolls'),
	path('exitpollupload/',views.exitpolladdform, name='exitpolladdform'),
]
