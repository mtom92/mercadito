from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from basics.models import MyUser, Business
from .forms import LoginForm, SignUpForm, BusinessForm, Search, FavoritesForm, SearchBusiness
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from mapbox import Geocoder
from . models import Business , Favorites, TypeBusiness, Category


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
            user = authenticate(username = u, password = p)
            print(user)
            if user is not None:
                if user. is_active:
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
            business = form.save(commit = False)
            geocoder = Geocoder(access_token="pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNqdWxveTFvMTI1N2Y0M25xZThwNnZ6Z3YifQ.9HGeUBB23XGsO1inCsw8vw")
            response = geocoder.forward(business.address, country=['us'])
            collection = response.json()
            coordinates = collection['features'][0]['geometry']['coordinates']
            business.location_latitude =coordinates[0]
            business.location_longitude =coordinates[1]
            business.owner = request.user
            business.save()
            return HttpResponseRedirect('/')
        else:
            print("form was not valid",form.errors, form.non_field_errors)
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
            else:
                businesses = []
            path = "/media/" + str(person.profile.avatar)
            print(businesses)
            return render(request, 'profile.html', {'person': person, 'path':path,"fav":fav,"businesses":businesses})

        else:
            person = MyUser.objects.get(id=id)
            path = "/media/" + str(person.profile.avatar)
            return render(request, 'profile.html', {'person': person, 'path':path})

    else:
        if Favorites.objects.filter(person_id=id):
            fav = Favorites.objects.filter(person_id=id)
            person = MyUser.objects.get(id=id)
            path = "http://localhost:8000/media/" + str(person.profile.avatar)
            return render(request, 'profile.html', {'person': person, 'path':path,"fav":fav})

        else:
            person = MyUser.objects.get(id=id)
            path = "/media/" + str(person.profile.avatar)
            return render(request, 'profile.html', {'person': person, 'path':path})


def business(request, id):
    if request.method == 'POST':
        form = FavoritesForm(request.POST)
        if form.is_valid():
            form.save()
            business = Business.objects.get(id=id)
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNqdWxveTFvMTI1N2Y0M25xZThwNnZ6Z3YifQ.9HGeUBB23XGsO1inCsw8vw'
            fav = Favorites.objects.filter(person_id=request.user.id)
            return render(request, 'business.html', {'business': business, 'mapbox': mapbox,"fav":fav})
        else:
            business = Business.objects.get(id=id)
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNqdWxveTFvMTI1N2Y0M25xZThwNnZ6Z3YifQ.9HGeUBB23XGsO1inCsw8vw'
            return render(request, 'business.html', {'business': business, 'mapbox': mapbox})

    else:
        business = Business.objects.get(id=id)
        if Favorites.objects.filter(person_id=request.user.id).filter(business_id=business.id):
            fav = Favorites.objects.filter(person_id=request.user.id)
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNqdWxveTFvMTI1N2Y0M25xZThwNnZ6Z3YifQ.9HGeUBB23XGsO1inCsw8vw'
            return render(request, 'business.html', {'business': business, 'mapbox': mapbox,"fav":fav})
        else:
            mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNqdWxveTFvMTI1N2Y0M25xZThwNnZ6Z3YifQ.9HGeUBB23XGsO1inCsw8vw'
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
            print("form was not valid",form.errors, form.non_field_errors)
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
            return render(request, 'search_result.html', {'result':result})
        else:
            print("form was not valid",form.errors)
            print("fields error", form.non_field_errors )
            return render(request, 'search.html', {'form': form})
    else:
        return render(request, 'search.html')

def searchb(request):
    print("estoy aqui !!")
    if request.method == 'GET':
        form = SearchBusiness(request.GET)
        print("this is the form",form)
        if form.is_valid():
            s = form.cleaned_data['type']
            result = Business.objects.filter(typebusiness_id=s)
            return render(request, 'search_result.html', {'result':result})
        else:
            print("form was not valid",form.errors)
            print("fields error", form.non_field_errors )
            return render(request, 'search.html', {'form': form})
    else:
        return render(request, 'search.html')


def load_categories(request):
    typebusiness_id = request.GET.get('typebusiness')
    categories = Category.objects.filter(typebusiness_id=typebusiness_id).order_by('name')
    return render(request, 'hr/category_dropdown_list_options.html', {'categories': categories})
