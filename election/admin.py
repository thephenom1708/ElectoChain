from django.contrib import admin
from .models import Candidate, Election

admin.site.register(Candidate)
admin.site.register(Election)