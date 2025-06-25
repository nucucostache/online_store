from django.shortcuts import render, redirect
from .models import Account
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login



def index(request):
    template = loader.get_template("accounts/login.html")
    return render(request, "accounts/login.html")


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # sau altă pagină după login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Poți crea aici UserProfile automat dacă vrei
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout(request):
    return HttpResponse('Va rog, sa iesiti de pe site!')




#----------------------------------------------------------------------------------









