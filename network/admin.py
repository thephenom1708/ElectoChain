from django.contrib import admin
from .models import Transaction, Block, Peer


admin.site.register(Transaction)
admin.site.register(Block)
admin.site.register(Peer)
