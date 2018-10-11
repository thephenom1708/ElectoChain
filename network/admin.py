from django.contrib import admin
from .models import Transaction, Block, Peer, Check


admin.site.register(Transaction)
admin.site.register(Block)
admin.site.register(Peer)
admin.site.register(Check)
