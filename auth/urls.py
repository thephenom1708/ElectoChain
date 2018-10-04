from django.conf.urls import url
from . import views

app_name = 'auth'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^loginVoter/$', views.loginVoter, name='loginVoter'),
    url(r'^validateVoter/$', views.validateVoter, name='validateVoter'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^addAdmin/$', views.addAdmin, name='addAdmin'),
    url(r'^loginAdmin/$', views.loginAdmin, name='loginAdmin'),
    url(r'^validateAdmin/$', views.validateAdmin, name='validateAdmin'),
    #url(r'^profile/$', views.profileView, name='profileView'),

]