from django.conf.urls import url
from . import views

app_name = 'election'

urlpatterns = [
    url(r'^createElection/(?P<ecId>\w+)/$', views.createElection, name='createElection'),
    url(r'^candidateList/(?P<voterId>\w+)/$', views.candidateList, name='candidateList'),
    url(r'^adminPanel/(?P<ecId>\w+)$', views.adminPanel, name='adminPanel'),
    url(r'^addCandidate/(?P<ecId>\w+)$', views.addCandidate, name='addCandidate'),
    url(r'^resultAnalysis/(?P<ecId>\w+)$', views.resultAnalysis, name='resultAnalysis')
]