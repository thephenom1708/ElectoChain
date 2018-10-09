from django.contrib import admin
from .models import Transaction, Block


admin.site.register(Transaction)
admin.site.register(Block)
