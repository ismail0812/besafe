import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from .models import CostumUser,Housedata,Cardata
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html', {})

@login_required(login_url="/login")
@csrf_exempt
def clientDashboard(request):
    user = request.user
    if request.method == "POST":
        # json.loads(request.body.decode())
        # print(json.loads(request.body.decode()))
        pass 
    return render(request, 'clientDashboard.html', {'user':user})

@login_required(login_url="/login")
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user':user})


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        passwd = request.POST.get("password")
        user = authenticate(request, username=email, password=passwd)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html', {})

def login_use(request):
    return render(request, 'login.html', {})

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        phone = request.POST.get("phone")
        birthday = request.POST.get("date")
        gender = request.POST.get("gender")
        passwd = request.POST.get("password")
        housedevice = request.POST.get('houseDevice')
        cardevice = request.POST.get('carDevice')
        CostumUser.object.create_user(email, passwd, )
        myuser = CostumUser.object.get(email = email)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.phone = phone
        myuser.gender = gender
        myuser.birthday = birthday
        myuser.housedevice_id = housedevice
        # myuser.cardevice_id = cardevice
        # myuser.is_activate = 0
        myuser.save()
        # return mediclainfos(request, myuser)
        return redirect('login')
    else:
        messages.error(request,'error')
    return render(request, 'signup.html', {})

def mediclainfos(request):
    if request.method == "POST":
        pass 
    return render(request, 'medical.html',{})

def loggout(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def storeHouseData(request):
    # Get the data from the POST request
    data = json.loads(request.body.decode())
    if CostumUser.objects.filter(housedevice_id=data['id']).exists():
        current_client = CostumUser.objects.get(housedevice_id=data['id'])
        # Store the data point in the database
        if Housedata.objects.filter(user = current_client).exists():
            Housedata.objects.filter(user = current_client).update(gas=data['gas'], fire=data['fire'], earthquake=data['earthquake'])
        else:
            data_point = Housedata(user=current_client, gas=data['gas'], fire=data['fire'], earthquake=data['earthquake'])
            data_point.save()

    return HttpResponse({'status': 'success'})

@csrf_exempt
def storeCarData(request):
    # Get the data from the POST request
    data = json.loads(request.body.decode())
    if CostumUser.objects.filter(cardevice_id=data['id']).exists():
        current_client = CostumUser.objects.get(cardevice_id=data['id'])
        # Store the data point in the database
        if Cardata.objects.filter(user = current_client).exists():
            Cardata.objects.filter(user = current_client).update(gas=data['gas'], fire=data['fire'], gps=str(data['gps']))
        else:
            data_point = Cardata(user=current_client, gas=data['gas'], fire=data['fire'], gps=str(data['gps']))
            data_point.save()
    return HttpResponse({'status': 'success'})

def data(request):
    current_client = request.user

# Get the latest data point for the current client
    
    latest_data_point = Housedata.objects.filter(user=current_client).order_by('-timestamp').first()
    latest_data_point2 = Cardata.objects.filter(user=current_client).order_by('-timestamp').first()
    # Return the latest data point as JSON
    return JsonResponse({'gas': latest_data_point.gas if latest_data_point else None,
                        'fire':latest_data_point.fire if latest_data_point else None,
                        'earthquake':latest_data_point.earthquake if latest_data_point else None,
                        'cargas': latest_data_point2.gas if latest_data_point2 else None,
                        'carfire':latest_data_point2.fire if latest_data_point2 else None,
                        'gps':latest_data_point2.gps if latest_data_point2 else None})