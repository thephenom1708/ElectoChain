from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.

class Voter(models.Model):
    aadhaar_id = models.CharField(max_length=16, primary_key=True)
    thumb_id = models.CharField(max_length=32)
    name = models.CharField(max_length=500)
    birth_date = models.DateField(null=True)
    age = models.IntegerField(default=0)
    profile_image = models.FileField(default="")
    locality = models.CharField(max_length=500)


    def __str__(self):
        return self.aadhaar_id + '-' + self.name


class ActiveVoter(models.Model):
    voter_id = models.CharField(max_length=500, primary_key=True)
    has_authenticated = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.voter_id + '-' + str(self.has_voted)


class Admin(models.Model):
    thumb_id = models.CharField(max_length=32)
    ec_id = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.ec_id;

