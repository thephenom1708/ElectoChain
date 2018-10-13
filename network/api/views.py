from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
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
    #print(transaction)
    newTransaction = Transaction()
    newTransaction.createNewTransaction(transaction['voter_id'], transaction['candidate_hash'])
    newTransaction.save()

    blockChain = getBlockchain()

    block = Block()
    block.createNewBlock(newTransaction.transaction_id, blockChain.blockList[-1])
    blockSerializer = BlockSerializer(block)
    #block.save()

    #print(json.dumps(blockSerializer.data))
    context = {
        'block': json.dumps(blockSerializer.data)
    }
    print(context['block'])
    return HttpResponse(json.dumps(context))


@csrf_exempt
def verifyBlock(request):
    block = json.loads(request.POST.get('block', None))

    """newBlock = Block()
    prevBlock = Block.objects.filter(hash=block['prev_hash'])[0]
    newBlock.createNewBlock(block['transaction_id'], prevBlock)"""

    success = False
    blockChain = getBlockchain()
    if len(blockChain.blockList) >= 3:
        for i in range(1, len(blockChain.blockList)+1):
            if(blockChain.blockList[i].hash == blockChain.blockList[i+1].prev_hash):
                success = True
            else:
                success = False
                break
    else:
        if(blockChain.blockList[-1].hash == block['prev_hash']):
            success = True

    if (success == True):
        context = {
            'success': True
        }
        return HttpResponse(json.dumps(context))
    else:
        context = {
            'success': False
        }
        return HttpResponse(json.dumps(context))




