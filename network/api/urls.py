from django.conf.urls import url
from . import views

urlpatterns = [
    url('^createBlock/', views.createBlock, name='createBlock'),
    url('^verifyBlock/', views.verifyBlock, name='verifyBlock')
]