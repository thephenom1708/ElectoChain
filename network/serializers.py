from rest_framework import serializers
from .models import Transaction, Block, Peer



class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields='__all__'


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model=Block
        fields='__all__'


class PeerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Peer
        fields = ('name', 'address',)
