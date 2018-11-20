from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from .forms import LoginForm


def signin(request):
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)

    if request.POST and form.is_valid():

        user = form.login()
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'signup/signin.html', {'form': form})


def signup(request):
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('home')
    else:
        form = UserCreationForm

    return render(request, 'signup/signup.html', {'form': form})


def signout(request):
    """
    :param request:
    :return:
    """
    logout(request)
    return redirect('sign')
