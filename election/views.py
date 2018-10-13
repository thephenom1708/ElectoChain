from django.shortcuts import render
from django.http import HttpResponse
from .models import Election, Candidate
from network.models import Block, Peer, Transaction
from .forms import ElectionForm
from .fusioncharts import FusionCharts
from collections import OrderedDict
import hashlib

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def adminPanel(request, ecId):
    if ecId is not None:
        elections = Election.objects.filter()
        context = {
            'elections': elections,
            'ecId': ecId,
        }
        return render(request, 'adminPanel.html', context)
    else:
        context = {
            'errMsg': 'Invalid Request ! Something went wrong !!!',
            'redirectLink': 'adminPanel.html'
        }
        return render(request, 'auth/error.html', context)



def createElection(request, ecId):
    elections = Election.objects.filter()
    if ecId is not None and request.method == "POST":

        newElection = Election()
        newElection.election_name = request.POST['electionName']
        newElection.election_region = request.POST['electionRegion']
        newElection.election_date = request.POST['electionDate']
        newElection.candidate_count = request.POST['candidateCount']
        newElection.election_description = request.POST['electionDescription']
        newElection.election_pic = request.FILES['electionPic']

        sha = hashlib.sha256()
        data = newElection.election_name + newElection.election_region;
        sha.update(data.encode('utf-8'))
        newElection.election_id = sha.hexdigest();

        file_type = newElection.election_pic.url.split('.')[-1]
        file_type = file_type.lower()

        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'election': newElection,
                'ecId': ecId,
                'errorMsg': 'Image file must be PNG, JPG, or JPEG',
                'elections': elections
            }
            return render(request, 'adminPanel.html', context)

        newElection.save()
        context = {
            'ecId': ecId,
            'successMsg': 'New election has been successfully Created !!!',
            'elections': elections
        }
        return render(request, 'adminPanel.html', context)

    else:
        context = {
            'ecId': ecId,
            'errMsg': 'Invalid Request ! Something went wrong !!!',
            'elections': elections
        }
        return render(request, 'adminPanel.html', context)



def addCandidate(request, ecId):
    elections = Election.objects.filter()
    if ecId is not None and request.method == "POST":
        newCandidate = Candidate()

        newCandidate.candidate_name = request.POST['candidateName']
        newCandidate.candidate_party = request.POST['candidateParty']
        newCandidate.candidate_age = request.POST['candidateAge']
        newCandidate.candidate_description = request.POST['candidateDescription']
        newCandidate.candidate_pic = request.FILES['candidatePic']

        electionId = request.POST['electionId']
        newCandidate.candidate_election = Election.objects.filter(election_id=electionId)[0]

        sha = hashlib.sha256()
        data = newCandidate.candidate_name + newCandidate.candidate_election.election_id + newCandidate.candidate_description;
        sha.update(data.encode('utf-8'))
        newCandidate.candidate_id = sha.hexdigest();

        file_type = newCandidate.candidate_pic.url.split('.')[-1]
        file_type = file_type.lower()

        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'candidate': newCandidate,
                'ecId': ecId,
                'errorMsg': 'Image file must be PNG, JPG, or JPEG',
                'elections': elections
            }
            return render(request, 'adminPanel.html', context)

        newCandidate.save()
        context = {
            'ecId': ecId,
            'successMsg': 'New Candidate has been successfully added to election Id '
                          + newCandidate.candidate_election.election_id + ' !!!',
            'elections': elections
        }
        return render(request, 'adminPanel.html', context)

    else:
        context = {
            'ecId': 'ecId',
            'errMsg': 'Invalid Request ! Something went wrong !!!',
            'elections': elections
        }
        return render(request, 'adminPanel.html', context)



def candidateList(request, voterId):
    if voterId is not None and request.session['voteCasted'] is False:
        currentElectionId = "feaaabeb4d6d00f5ec2c3eed5d6987566cbeedca9213d7be17534fa537fc0154"
        currentElection = Election.objects.filter(election_id=currentElectionId)[0]
        candidates = Candidate.objects.filter(candidate_election=currentElection)

        context = {
            'voterId': voterId,
            'candidates': candidates,
            'currentElection': currentElection
        }
        return render(request, 'election/candidateList.html', context)
    else:
        context = {
            'voterId': voterId,
            'errorMsg': 'You have already casted your vote !'
        }
        return render(request, 'election/candidateList.html', context)


def getVoteCount(candidate):
    blockList = Block.objects.filter()

    voteCount = 0
    for block in blockList:
        transactionId = block.transaction_id
        transaction = Transaction.objects.filter(transaction_id=transactionId)[0]

        sha = hashlib.sha256()
        data = candidate.candidate_id + transaction.salt
        sha.update(data.encode('utf-8'))
        hash = sha.hexdigest();

        if(hash == transaction.candidate_hash):
            voteCount += 1

    return voteCount


def resultAnalysis(request, ecId):
    if ecId is not None:
        chartConfig = OrderedDict()
        chartConfig["caption"] = "Loksabha Elections : 2019"
        chartConfig["subCaption"] = "The Voting count"
        chartConfig["xAxisName"] = "Candidates"
        chartConfig["yAxisName"] = "No. of Votes"
        chartConfig["numberSuffix"] = ""
        chartConfig["theme"] = "fusion"

        currentElectionId = "feaaabeb4d6d00f5ec2c3eed5d6987566cbeedca9213d7be17534fa537fc0154"
        currentElection = Election.objects.filter(election_id=currentElectionId)[0]
        candidates = Candidate.objects.filter(candidate_election=currentElection)

        chartData = OrderedDict()
        for candidate in candidates:
            count = getVoteCount(candidate)
            chartData[candidate.candidate_name] = count

        dataSource = {}
        dataSource["chart"] = chartConfig
        dataSource["data"] = []

        for key, value in chartData.items():
            data = {}
            data["label"] = key
            data["value"] = value
            dataSource["data"].append(data)


        column2D = FusionCharts("column2d", "myFirstChart", "800", "400", "myFirstchart-container", "json", dataSource)

        return render(request, 'results/resultAnalysis.html', {
            'output': column2D.render(),
            'ecId': ecId
        })


