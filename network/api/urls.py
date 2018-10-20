from django.conf.urls import url
from . import views

urlpatterns = [
    url('^requestLock/', views.requestLock, name='requestLock'),
    url('^freeLock/', views.freeLock, name='freeLock'),
    url('^createBlock/', views.createBlock, name='createBlock'),
    url('^verifyBlock/', views.verifyBlock, name='verifyBlock'),
    url('^blockAcception/', views.blockAcception, name='blockAcception'),
    url('^requestBlockchain/', views.requestBlockchain, name='requestBlockchain')
]