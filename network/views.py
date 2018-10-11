from django.shortcuts import render
from django.http import HttpResponse
from .models import Transaction, Block, Peer
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
            newTransaction.save()
            request.session['voteCasted'] = True

            transaction = TransactionSerializer(newTransaction)
            peerNodes = Peer.objects.filter()

            a = []
            for peer in peerNodes:
                print("sending to ", peer.address)
                address = "http://" + peer.address + "/network/api/createBlock/"
                context = {
                    'transaction': json.dumps(transaction.data)
                }
                requests.post(address, data=context)





@csrf_exempt
def receiveTransaction(request):
    context = {
        'transaction': request.POST.get('transaction', None)
    }
    return HttpResponse(json.dumps(context))

