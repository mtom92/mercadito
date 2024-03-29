from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from basics.models import MyUser, Business
from .forms import LoginForm, SignUpForm, BusinessForm, Search, FavoritesForm, SearchBusiness
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from mapbox import Geocoder
from .models import Business, Favorites, TypeBusiness, Category
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
import os
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings



def index(request):
    print("home route")
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
                messages.error(request, 'The username and/or password is incorrect.')
                return HttpResponseRedirect('/login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def newbusiness(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            geocoder = Geocoder(
                access_token="pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNscDRtdzZhejB5bGYya21pcXllaGphM2kifQ.CPoqHJARN8PAAZ493bWvjg")
            response = geocoder.forward(business.address, country=['us'])
            collection = response.json()
            coordinates = collection['features'][0]['geometry']['coordinates']
            business.location_latitude = coordinates[0]
            business.location_longitude = coordinates[1]
            business.owner = request.user
            business.save()
        else:
            print("form was not valid", form.errors, form.non_field_errors)
            return render(request, 'signup.html', {'form': form})
    else:
        form = BusinessForm()
    return render(request, 'newbusiness.html', {'form': form})


def profile(request, id):
    if request.user.type_of_user == 'business_owner':
        if Favorites.objects.filter(person_id=id):
            fav = Favorites.objects.filter(person_id=id)
            person = MyUser.objects.get(id=id)
            if Business.objects.filter(owner=id):
                businesses = Business.objects.filter(owner=id)
                print(businesses, id)
            else:
                businesses = []
            path = "/media/" + str(person.profile.avatar)
            print(businesses)
            return render(request, 'profile.html',
                          {'person': person, 'path': path, "fav": fav, "businesses": businesses})

        else:
            person = MyUser.objects.get(id=id)
            if Business.objects.filter(owner=id):
                businesses = Business.objects.filter(owner=id)
                print(businesses, id)
            else:
                businesses = []
            path = "/media/" + str(person.profile.avatar)
            return render(request, 'profile.html', {'person': person, 'path': path, "businesses": businesses})

    else:
        if Favorites.objects.filter(person_id=id):
            fav = Favorites.objects.filter(person_id=id)
            person = MyUser.objects.get(id=id)
            path = "/media/" + str(person.profile.avatar)
            return render(request, 'profile.html', {'person': person, 'path': path, "fav": fav})

        else:
            person = MyUser.objects.get(id=id)
            path = "/media/" + str(person.profile.avatar)
            return render(request, 'profile.html', {'person': person, 'path': path})


def business(request, id):
    if request.method == 'POST':
        form = FavoritesForm(request.POST)
        if form.is_valid():
            form.save()
            business = Business.objects.get(id=id)
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNscDRtdzZhejB5bGYya21pcXllaGphM2kifQ.CPoqHJARN8PAAZ493bWvjg'
            fav = Favorites.objects.filter(person_id=request.user.id)
            return render(request, 'business.html', {'business': business, 'mapbox': mapbox, "fav": fav})
        else:
            business = Business.objects.get(id=id)
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNscDRtdzZhejB5bGYya21pcXllaGphM2kifQ.CPoqHJARN8PAAZ493bWvjg'
            return render(request, 'business.html', {'business': business, 'mapbox': mapbox})

    else:
        business = Business.objects.get(id=id)
        if Favorites.objects.filter(person_id=request.user.id).filter(business_id=business.id):
            fav = Favorites.objects.filter(person_id=request.user.id)
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNscDRtdzZhejB5bGYya21pcXllaGphM2kifQ.CPoqHJARN8PAAZ493bWvjg'
            return render(request, 'business.html', {'business': business, 'mapbox': mapbox, "fav": fav})
        else:
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNscDRtdzZhejB5bGYya21pcXllaGphM2kifQ.CPoqHJARN8PAAZ493bWvjg'
            return render(request, 'business.html', {'business': business, 'mapbox': mapbox})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.avatar = form.cleaned_data.get('avatar')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            print("form was not valid", form.errors, form.non_field_errors)
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def search(request):
    if request.method == 'GET':
        form = Search(request.GET)
        if form.is_valid():
            s = form.cleaned_data['searcher']
            result = Business.objects.filter(name__icontains=s)
            return render(request, 'search_result.html', {'result': result})
        else:
            print("form was not valid", form.errors)
            print("fields error", form.non_field_errors)
            return render(request, 'search.html', {'form': form})
    else:
        return render(request, 'search.html')


def searchb(request):
    print("estoy aqui !!")
    if request.method == 'GET':
        form = SearchBusiness(request.GET)
        print("this is the form", form)
        if form.is_valid():
            s = form.cleaned_data['type']
            result = Business.objects.filter(typebusiness_id=s)
            return render(request, 'search_result.html', {'result': result})
        else:
            print("form was not valid", form.errors)
            print("fields error", form.non_field_errors)
            return render(request, 'search.html', {'form': form})
    else:
        return render(request, 'search.html')


def load_categories(request):
    typebusiness_id = request.GET.get('typebusiness')
    categories = Category.objects.filter(typebusiness_id=typebusiness_id).order_by('name')
    return render(request, 'hr/category_dropdown_list_options.html', {'categories': categories})


@csrf_exempt
def webhook(request):
    account_sid = 'AC9030fb8d0a2e52b72adcdb6b45de368d'
    auth_token = os.environ.get('TWILIO_TOKEN', '')
    client = Client(account_sid, auth_token)
    phone_number_from = request.POST.get('From', '')
    phone_number_to = request.POST.get('To', '')
    msg = request.POST.get('Body', '')
    msg = msg.lower()
    response = "Sorry, I'm still learning"

    if 'hi' in msg or 'hey' in msg or 'hello' in msg:
        response = 'Hello! How can I help?'
    elif 'open a business' in msg:
        response = 'Great! What type of business do you have'
    elif 'food' in msg:
        response = 'Here is some information that you might need' + \
                   '\nBusiness license required by the WA govt' + \
                   '\nLicense required by the IRS'
    elif 'insurance' in msg:
        response = 'Yes, you will need insurance copies to be submitted to get these licenses'
    elif 'spanish' in msg or 'espanol' in msg or 'español' in msg:
        response = 'Sí, también hablo español. Podemos continuar'
    elif 'negocio de comida' in msg or 'restaurante' in msg or 'taqueria' in msg:
        response = "Estos son los requisitos para un negocio de comida" + \
                   '\nLicencia de negocio requerida por el gobierno de WA' + \
                   '\nLicencia requerida por el IRS'

    message = client.messages.create(
        from_=phone_number_to,
        body=response,
        to=phone_number_from
    )

    print(message.sid)
    return HttpResponse("OK")
