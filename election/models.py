from django.db import models


class Election(models.Model):
    election_id = models.CharField(primary_key=True, max_length=100)
    election_name = models.CharField(max_length=50)
    election_region = models.CharField(max_length=50, default="")
    election_date = models.DateField(null=True)
    candidate_count = models.IntegerField(default=0)
    election_description = models.TextField(max_length=500, default="")
    election_pic = models.FileField(null=True)


    def __str__(self):
        return str(self.election_id) + '-' + str(self.election_name)


class Candidate(models.Model):
    candidate_id = models.CharField(max_length=100, primary_key=True)
    candidate_name = models.CharField(max_length=30)
    candidate_party = models.CharField(max_length=30)
    candidate_age = models.CharField(max_length=30)
    candidate_description = models.CharField(max_length=500)
    candidate_pic = models.FileField()
    candidate_election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return self.candidate_id + '-' + self.candidate_name

