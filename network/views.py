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
def broadcastBlock(serializedBlock, peer, validatePackets):
    context = {
        'block':json.dumps(serializedBlock.data)
    }
    address = "http://" + peer.address + "/network/api/verifyBlock/"
    response = requests.post(address, data=context)
    response = json.loads(response.content)
    validatePackets.append(response)
    return HttpResponse(json.dumps(response))


@csrf_exempt
def blockAcception(serializedBlock, peer):
    context = {
        'block': json.dumps(serializedBlock.data)
    }
    address = "http://" + peer.address + "/network/api/blockAcception/"
    requests.post(address, data=context)
    return

@csrf_exempt
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

            #transaction Broadcasting...
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

            #Block Broadcasting and Verifying...
            newBlock = Block()
            prevBlock = Block.objects.filter(hash=block['prev_hash'])[0]
            newBlock.createNewBlock(block['transaction_id'], prevBlock)
            blockSerializer = BlockSerializer(newBlock)

            validatePackets = []
            for peer in peerNodes:
                t = ThreadWithReturnValue(target=broadcastBlock, args=(blockSerializer, peer, validatePackets))
                threads.append(t)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            #Counting Success packets...
            successPackets = 0
            failurePackets = 0
            successHost = None
            failureHost = None
            for packet in validatePackets:
                print(packet)
                if packet['success'] is True:
                    successPackets += 1
                    successHost = packet['host']
                else:
                    failurePackets += 1
                    failureHost = packet['host']

            #Block Acception and Fault Tolerance...
            threads.clear()
            if(successPackets >= failurePackets):
                for peer in peerNodes:
                    t = threading.Thread(target=blockAcception, args=(blockSerializer, peer))
                    threads.append(t)

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                for packet in validatePackets:
                    if packet['success'] is False:
                        address = "http://" + successHost + "/network/api/requestBlockchain/"
                        context = {
                            'peer':packet['host']
                        }
                        requests.post(address, data=context)

                return HttpResponse("Your vote has been successfully casted !!!")

            else:
                return HttpResponse("Your vote has not been casted ! Please try again !!!" + str(failurePackets))


@csrf_exempt
def receiveTransaction(request):
    context = {
        'transaction': request.POST.get('transaction', None)
    }
    print("Success Achieved")
    print(json.dumps(context))
    #return HttpResponse(json.dumps(context))
