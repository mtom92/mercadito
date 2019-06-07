from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from basics.models import MyUser, Business
from .forms import LoginForm , SignUpForm, BusinessForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
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
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit = False)
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
    user = MyUser.objects.get(id=id)
    path = "http://localhost:8000/media/" + str(user.profile.avatar)
    return render(request, 'profile.html', {'user': user, 'path':path})

def business(request, id):
    business = Business.objects.get(id=id)
    mapbox = 'pk.eyJ1IjoibXRvbTkyIiwiYSI6ImNqdWxveTFvMTI1N2Y0M25xZThwNnZ6Z3YifQ.9HGeUBB23XGsO1inCsw8vw'
    return render(request, 'business.html', {'business': business, 'mapbox': mapbox})


def signup(request):
    if request.method == 'POST':
        print(request.FILES)
        context = {}
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
