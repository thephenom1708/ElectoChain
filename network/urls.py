from django.conf.urls import url
from . import views

app_name = 'network'

urlpatterns = [
    url('^createTransaction/(?P<candidateId>\w+)/$', views.createNewTransaction, name='createNewTransaction'),

]