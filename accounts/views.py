from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from .forms import CustomAuthenticationForm
def signupaccount(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email=form.cleaned_data['email']
            try:
                user = User.objects.create_user(username=username, password=password,email=email)
                user.save()
                login(request, user)
                return redirect('index')  # Redirect to home page or desired page
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form': form, 'error': 'Username already taken. Choose a new username.'})
        else:
            return render(request, 'signupaccount.html', {'form': form, 'error': 'Form is not valid'})
    else:
        form = UserCreateForm()
    return render(request, 'signupaccount.html', {'form': form})


def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': CustomAuthenticationForm()})
    else:
        form = CustomAuthenticationForm(request.POST)
        user = authenticate(
            request,
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )
        if user is None:
            return render(request, 'loginaccount.html', {'form': form, 'error': 'Username and password do not match'})
        else:
            login(request, user)
            return redirect('index')

def logoutaccount(request):
    logout(request)
    return redirect('index')