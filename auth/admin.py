from django.contrib import admin
from .models import Voter, ActiveVoter, Admin

admin.site.register(Voter)
admin.site.register(ActiveVoter)
admin.site.register(Admin)