from decimal import Decimal
from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from User.models import ComputerType
from .forms import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'staff/index.html')

def computer_types(request):
    if request.method == 'POST':
        form = AddComputerTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Computer")
            return redirect('staff:computer_types')
    return render(request, 'staff/computer_types.html', {
        "computers": ComputerType.objects.all(),
        "AddComputerTypeForm": AddComputerTypeForm()
    })

def add_computer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')
        price_per_hour = request.POST.get('price_per_hour')
        graphics_card = request.POST.get('graphics_card')
        ram = request.POST.get('ram')
        cpu = request.POST.get('cpu')
        storage = request.POST.get('storage')
        ComputerType.objects.create(
            name=name,
            status=status,
            price_per_hour=price_per_hour,
            graphics_card=graphics_card,
            ram=ram,
            cpu=cpu,
            storage=storage,
        )
    return render(request, 'staff/computer_types.html')

def edit_computer(request, computer_id):
    computer = ComputerType.objects.get(id=computer_id)
    if request.method == 'POST':
        form = EditComputerTypeForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            messages.success(request, "Edited Computer")
            return redirect('staff:computer_types')
    return render(request, 'staff/computer_types_edit.html', {
        "computer": computer,
        "form": EditComputerTypeForm(instance=computer)
    })

def delete_computer(request, computer_id):
    computer = ComputerType.objects.get(id=computer_id)
    computer.delete()
    return redirect('staff:computer_types')

def view_computer_type(request, computer_id):
    computer = ComputerType.objects.get(id=computer_id)
    return render(request, 'staff/view_computer_type.html', {
        "computer": computer
    })

# Computer List
def computer_list(request):
    type_id = request.GET.get('computer_type_id')
    computer_ls = ComputerList.objects.all()
    if type_id:
        computer_ls = computer_ls.filter(computer_type_id=type_id)
    return render(request, 'staff/computer_list.html', {
        "computer_list": computer_ls,
        "computer_types": ComputerType.objects.all(),
        "form": AddComputerListForm()
    })
def computer_list_add(request):
    if request.method == 'POST':
        form = AddComputerListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Computer to List")
        return redirect('staff:computer_list')
    return render(request, 'staff/computer_list_submit.html', {
        "form": AddComputerListForm()
    })
def computer_list_edit(request, computer_id):
    computer = ComputerList.objects.get(id=computer_id)
    if request.method == 'POST':
        form = AddComputerListForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            messages.success(request, "Edited Computer in List")
            return redirect('staff:computer_list')
    return render(request, 'staff/computer_list_submit.html', {
        "form": AddComputerListForm(instance=computer)
    })
def computer_list_delete(request, computer_id):
    computer = ComputerList.objects.get(id=computer_id)
    computer.delete()
    return redirect('staff:computer_list')

def test(request):
    computers_list = ComputerList.objects.all()
    users = User.objects.all()
    sessions = Session.objects.all()
    return render(request, 'staff/test.html', {
        'computers_list': computers_list,
        'users': users,
        'sessions': sessions
    })

def play(request, computer_id):
    users = User.objects.all()
    if(request.method == "POST"):
        user_id = request.POST.get('user')
        user = User.objects.get(id=user_id)
        computer_object = ComputerList.objects.get(id=computer_id)

        Session.objects.create(
            user=user, 
            pc=computer_object, 
            start_time=timezone.now(), 
            price_per_hour=computer_object.computer_type.price_per_hour,    
            is_active=True
        )
        computer_object.is_active = True
        computer_object.save()
        return redirect('staff:test')
    
    avaiable_computers = ComputerList.objects.filter(is_active=False)
    return render(request, 'staff/play.html', {
        'computer_id': computer_id, 
        'avaiable_computers': avaiable_computers,
        'users': users
    })

def stop(request, computer_id):
    if (request.method == "POST"):
        computer_object = ComputerList.objects.get(id=computer_id)

        active_session = Session.objects.get(pc=computer_object, is_active=True)
        active_session.end_time = timezone.now()
        computer_object.is_active = False
        active_session.is_active = False
        active_session.end_time = timezone.now()
        # Tính chi phí
        total_seconds_played = (active_session.end_time - active_session.start_time).total_seconds()
        price_per_second = active_session.price_per_hour / Decimal(3600)
        active_session.cost = Decimal(total_seconds_played) * price_per_second
        # Trừ tiền người dùng
        user_object = active_session.user
        user_object.money_left -= active_session.cost
        user_object.save()
        # Lưu lại
        active_session.save()
        computer_object.save()
        return redirect('staff:test')
    return render(request, 'staff/stop.html', {
        'computer_id': computer_id
    })