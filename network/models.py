from django.db import models
from auth.models import ActiveVoter
import hashlib
import random
import secrets
import time
import json


class Transaction(models.Model):
    voter = models.ForeignKey(ActiveVoter, on_delete=models.CASCADE)
    salt = models.CharField(max_length=100)
    candidate_hash = models.CharField(max_length=100)

    def setTransaction(self, voter, candidateId):
        self.voter = voter
        self.salt = secrets.token_hex(5)
        self.calculateCandidateHash(candidateId)

    def calculateCandidateHash(self, candidateId):
        sha = hashlib.sha256()
        data = candidateId + str(self.salt)
        sha.update(data.encode('utf-8'))
        self.candidate_hash = sha.hexdigest()

    def __str__(self):
        return str(self.voter.voter_id) + '--' + str(self.candidate_hash)


class Block(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    prev_hash = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    def __init__(self, transaction, prevBlock):
        self.transaction = transaction
        self.prev_hash = prevBlock.prev_hash
        self.nonce = 0;
        self.difficulty = 5;

    def generateHash(self):
        sha = hashlib.sha256()
        data = str(self.timestamp) + self.prev_hash + str(self.transaction)
        sha.update(data.encode('utf-8'))
        hash = sha.hexdigest()
        return hash

    def mineBlock(self):
        target = str('0' * self.difficulty)
        while str(self.hash[:self.difficulty]) != target:
            self.nonce = self.nonce + 1
            self.hash = self.generateHash()



