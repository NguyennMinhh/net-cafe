from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Menu, Session
from decimal import Decimal

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

def session_view(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'POST':
        if 'start_session' in request.POST:
            # tạo object session mới
            Session.objects.create(user=request.user, start_time=timezone.now())
            return redirect('user:session')

        if 'end_session' in request.POST:
            session = Session.objects.filter(user=request.user, end_time__isnull=True).first()
            if session:
                session.end_time = timezone.now()
                # trừ tiền với giá 10k/giờ
                total_time_played = Decimal((session.end_time - session.start_time).total_seconds()) / Decimal(3600)
                if total_time_played < (1/60):  # phòng trường hợp nhỏ hơn 1 phút
                    total_time_played = Decimal(1) / Decimal(60)
                session.cost = Decimal(total_time_played * session.price_per_hour).quantize(Decimal('0.01'))
                session.is_active = False
                session.save()
                # trừ tiền user
                request.user.money_left -= session.cost
                request.user.save()
            return redirect('user:index')

    return render(request, 'user/session.html')