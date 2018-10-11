from django.db import models


# Create your models here.

class Transaction(models.Model):
    voterId=models.CharField(max_length=256)
    salt=models.CharField(max_length=10)
    candidateHash=models.CharField(max_length=256)

    def __str__(self):
        return self.voterId



class Block(models.Model):
    timeStamp=models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    previousHash=models.CharField(max_length=256)
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE)
    nonce=models.IntegerField(default=0)
    hash=models.CharField(max_length=256)