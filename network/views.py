from django.shortcuts import render
from django.http import HttpResponse
from .models import Transaction, Block
from auth.models import ActiveVoter

def createNewTransaction(request, candidateId):
    if candidateId is not None:
        voterId = request.session['voterId']
        currentVoter = ActiveVoter.objects.filter(voter_id=voterId)[0]

        if currentVoter is not None:
            newTransaction = Transaction()
            newTransaction.setTransaction(currentVoter, candidateId)
            newTransaction.save()
            request.session['voteCasted'] = True
            return HttpResponse("Hello")
