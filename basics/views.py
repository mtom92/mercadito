from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from basics.models import MyUser
from .forms import LoginForm , SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
import os

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


def profile(request, id):
    user = MyUser.objects.get(id=id)
    path = "http://localhost:8000/" + str(user.profile.avatar)
    return render(request, 'profile.html', {'user': user, 'path':path})


def signup(request):
    if request.method == 'POST':
        print(request.FILES)
        context = {}
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['avatar']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
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
