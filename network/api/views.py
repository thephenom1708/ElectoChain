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
import requests

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
    newTransaction.transaction_id = transaction['transaction_id']
    newTransaction.voter_id = transaction['voter_id']
    newTransaction.salt = transaction['salt']
    newTransaction.candidate_hash = transaction['candidate_hash']
    newTransaction.save()

    blockChain = getBlockchain()

    block = Block()
    block.createNewBlock(newTransaction.transaction_id, blockChain.blockList[-1])
    blockSerializer = BlockSerializer(block)

    #print(json.dumps(blockSerializer.data))
    context = {
        'block': json.dumps(blockSerializer.data)
    }
    print(context['block'])
    return HttpResponse(json.dumps(context))


@csrf_exempt
def verifyBlock(request):
    block = json.loads(request.POST.get('block', None))

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
            'success': True,
            'host': request.get_host()
        }
        return HttpResponse(json.dumps(context))
    else:
        context = {
            'success': False,
            'host': request.get_host()
        }
        return HttpResponse(json.dumps(context))

@csrf_exempt
def blockAcception(request):
    block = json.loads(request.POST.get('block', None))
    if block is not None:
        newBlock = Block()
        newBlock.timestamp = block['timestamp']
        newBlock.transaction_id = block['transaction_id']
        newBlock.prev_hash = block['prev_hash']
        newBlock.hash = block['hash']

        newBlock.save()

    return

@csrf_exempt
def requestBlockchain(request):
    blockList = list(Block.objects.filter())

    peerAddress = request.POST.get('peer', None)

    address = "http://" + peerAddress + "/network/api/replaceBlockchain/"
    context = {
        'blockList': json.dumps(blockList)
    }
    requests.post(address, data=context)
    return


@csrf_exempt
def replaceBlockchain(request):
    blockList = json.loads(request.POST.get('blockList', None))

    if blockList is not None:
        Block.objects.all().delete()
        for block in blockList:
            block.save()

    return





