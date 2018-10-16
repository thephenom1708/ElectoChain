from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import hashlib
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q
from .models import Voter, ActiveVoter, Admin
from election.models import Election
from .forms import AdminForm
# Create your views here.

def index(request):
    if 'admin' in request.session:
        return render(request, 'index.html')
    else:
        request.session['admin'] = None
        request.session['has_authenticated'] = False
        return render(request, 'index.html')



def loginVoter(request):
    if request.session['has_authenticated'] is not True and request.session['admin'] is not True:
        return render(request, 'auth/loginVoter.html')
    else:
        context = {
            'errorMsg': 'You are already Logged in !!!',
            'voterId': request.session['voterId']
        }
        return render (request, 'auth/loginVoter.html', context)



def logout(request):
    if request.session['admin'] is True:
        request.session['admin'] = None
        request.session['ecId'] = None
        return render(request, 'index.html')

    elif request.session['voterId'] is not None:
        request.session['voterId'] = None
        request.session['has_authenticated'] = None
        request.session['has_voted'] = None
        return render(request, 'index.html')

    else:
        context = {
            'errMsg': 'Invalid Logout request !!!',
        }
        return render(request, 'auth/error.html', context)



def validateVoter(request):
    if request.method == 'POST':
        thumbId = request.POST['thumbId']
        aadhaarId = request.POST['aadhaarId']
        voter = Voter.objects.filter(thumb_id=thumbId, aadhaar_id=aadhaarId)
        if not voter:
            return render(request, 'auth/loginVoter.html', { 'validate': False })
        else:
            #Generating Voter_ID...
            sha = hashlib.sha256()
            voterData = voter[0].aadhaar_id + voter[0].name + str(voter[0].birth_date) + voter[0].locality
            sha.update(voterData.encode('utf-8'))
            voterId = sha.hexdigest()

            activeVoter = ActiveVoter.objects.filter(voter_id=voterId)

            if not activeVoter:
                #Adding the authenticated voter to database..
                activeVoter = ActiveVoter()
                activeVoter.voter_id = voterId
                activeVoter.has_authenticated = True
                activeVoter.save()
                request.session['voterId'] = voterId
                request.session['has_authenticated'] = True
                request.session['has_voted'] = False
                request.session['voteCasted'] = False

                return render(request, 'auth/profile.html', { 'activeVoter': activeVoter, 'voterInfo': voter[0] })
            else:
                request.session['voterId'] = voterId
                request.session['has_authenticated'] = True
                request.session['has_voted'] = False
                request.session['voteCasted'] = False
                return render(request, 'auth/profile.html', {'activeVoter': activeVoter[0], 'voterInfo': voter[0]})



def loginAdmin(request):
    if request.session['admin'] is True:
        context = {
            'errMsg': 'You are already logged in as Admin !!!',
            'redirectLink': 'adminPanel',
        }
        return render(request, 'auth/error.html', context)

    else:
        form = AdminForm(request.POST or None)
        if form.is_valid():
            thumbId = form.cleaned_data['thumb_id']
            password = form.cleaned_data['password']

            sha = hashlib.sha256()
            data = thumbId + password;
            sha.update(data.encode('utf-8'))
            ecId = sha.hexdigest();

            activeAdmin = Admin.objects.filter(thumb_id=thumbId, ec_id=ecId)
            if not activeAdmin:
                context = {
                    'validate': False,
                    'form': form
                }
                return render(request, 'auth/loginAdmin.html', context)
            else:
                request.session['admin'] = True
                request.session['ecId'] = activeAdmin[0].ec_id

                elections = Election.objects.filter()
                context = {
                    'ecId': activeAdmin[0].ec_id,
                    'elections': elections,
                }

                return render(request, 'adminPanel.html', context)
        context = {
            "form": form,
        }
        return render(request, 'auth/loginAdmin.html', context)



def addAdmin(request):
    form = AdminForm(request.POST or None)
    if form.is_valid():
        thumbId = form.cleaned_data['thumb_id']
        password = form.cleaned_data['password']

        sha = hashlib.sha256()
        data = thumbId + password;
        sha.update(data.encode('utf-8'))
        ecId = sha.hexdigest();

        admin = Admin()
        admin.thumb_id = thumbId
        admin.ec_id = ecId

        admin.save()
        return render(request, 'index.html')

    context = {
        "form": form,
    }
    return render(request, 'auth/addAdmin.html', context)



def validateAdmin(request):
    if request.method == 'POST':
        thumbId = request.POST['thumbId']
        ecId = request.POST['ecId']
        password = request.POST['password']

        admin = Admin.objects.filter(thumb_id=thumbId, ec_id=ecId, password=password)
        if not admin:
            return render(request, 'auth/loginAdmin.html', {'validate': False})
        else:
            return HttpResponse("Admin Section")


