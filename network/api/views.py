from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from network.serializers import BlockSerializer, PeerSerializer, TransactionSerializer
from network.models import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
class Blockchain(object):

    @csrf_exempt
    def __init__(self):
        self.blockList = []
        self.openTransactions = []

    @csrf_exempt
    def createBlockchain(self, blockList, openTransactions):
        self.blockList = blockList
        self.openTransactions = openTransactions

@csrf_exempt
def getBlockchain():
    blockList = list(Block.objects.filter())
    openTransactions = Transaction.objects.filter()

    blockchain = Blockchain()
    blockchain.createBlockchain(blockList, openTransactions)
    return blockchain



@csrf_exempt
def createBlock(request):
    transaction = json.loads(request.POST.get('transaction', None))
    print(transaction)
    newTransaction = Transaction()
    newTransaction.createNewTransaction(transaction['voter_id'], transaction['candidate_hash'])

    blockChain = getBlockchain()
    print("Hello")
    block = Block()
    block.transaction = newTransaction
    block.prev_hash = blockChain.blockList[-1].hash
    block.nonce = 0
    block.difficulty = 5
    block.mineBlock()

    #block.createNewBlock(newTransaction, blockChain.blockList[-1])
    blockSerializer = BlockSerializer(block)
    block.save()
    print("Hello There")
    headers = request.get_success_headers(blockSerializer.data)
    print(blockSerializer.data)
    return Response(blockSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
