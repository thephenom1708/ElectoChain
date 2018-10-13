from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Transaction, Block, Peer
from .api.views import getBlockchain, Blockchain
from auth.models import ActiveVoter
from .serializers import TransactionSerializer, BlockSerializer, PeerSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json, requests
from json import JSONEncoder, JSONDecoder
from django.urls import reverse
from .utils import JsonApi
import threading
from threading import Thread


@csrf_exempt
def broadcastTransaction(serializedTransaction, peer):
    context = {
        'transaction':json.dumps(serializedTransaction.data)
    }
    address = "http://" + peer.address + "/network/api/createBlock/"
    response = (requests.post(address, data=context))
    response = json.loads(response.content)
    return HttpResponse(json.dumps(response))


@csrf_exempt
def broadcastBlock(serializedBlock, peer):
    context = {
        'block':json.dumps(serializedBlock.data)
    }
    address = "http://" + peer.address + "/network/api/verifyBlock/"
    response = requests.post(address, data=context)
    return HttpResponse(response)


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return



@csrf_exempt
def castNewVote(request, candidateId):
    """if candidateId is not None:
        voterId = request.session['voterId']
        currentVoter = ActiveVoter.objects.filter(voter_id=voterId)[0]
        if currentVoter is not None:
            #Transaction Creation...
            newTransaction = Transaction()
            newTransaction.createNewTransaction(currentVoter, candidateId)
            newTransaction.save()
            request.session['voteCasted'] = True
            transaction = TransactionSerializer(newTransaction)
            peerNodes = Peer.objects.filter()

            a = []
            for peer in peerNodes:
                address = "http://" + peer.address + "/network/newTransaction/"
                context = {
                    'transaction': json.dumps(transaction.data)
                }
                response = requests.post(address, data=context)
                a.append(response)
            return HttpResponse(a[1])"""

    if candidateId is not None:
        voterId = request.session['voterId']
        currentVoter = ActiveVoter.objects.filter(voter_id=voterId)[0]

        if currentVoter is not None:
            # Transaction Creation...
            newTransaction = Transaction()
            newTransaction.createNewTransaction(voterId, candidateId)

            request.session['voteCasted'] = True

            transaction = TransactionSerializer(newTransaction)
            peerNodes = Peer.objects.filter()

            threads = []
            for peer in peerNodes:
                print("sending to ", peer.address)
                t = ThreadWithReturnValue(target=broadcastTransaction, args=(transaction, peer,))
                threads.append(t)

            response = ""
            for thread in threads:
                thread.start()

            for thread in threads:
                response = thread.join()
                if response is not None:
                    break

            response = json.loads(response.content)
            responseBlock = json.loads(response['block'])

            threads.clear()
            if response is not None:
                block = responseBlock
            else:
                return HttpResponse("Block Mining Failed !!!")


            newBlock = Block()
            prevBlock = Block.objects.filter(hash=block['prev_hash'])[0]
            newBlock.createNewBlock(block['transaction_id'], prevBlock)
            blockSerializer = BlockSerializer(newBlock)

            for peer in peerNodes:
                t = ThreadWithReturnValue(target=broadcastBlock, args=(blockSerializer, peer,))
                threads.append(t)

            validatePackets = []
            for thread in threads:
                thread.start()

            for thread in threads:
                responsePacket = thread.join()
                validatePackets.append(responsePacket)

            return HttpResponse(str(len(validatePackets)))


@csrf_exempt
def receiveTransaction(request):
    context = {
        'transaction': request.POST.get('transaction', None)
    }
    print("Success Achieved")
    print(json.dumps(context))
    #return HttpResponse(json.dumps(context))
