from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Menu

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))
    return render(request, 'user/index.html', {
        "user": request.user,
        "menu": Menu.objects.all(),
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:index')
        return render(request, 'user/login.html', {'notification':'Invalid credentials'})
    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return redirect('user:login')