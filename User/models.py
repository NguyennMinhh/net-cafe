from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    money_left = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Menu(models.Model):
    picture = models.URLField(max_length=300)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}đ"

# Quản lý các loại máy tính:
class ComputerType(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    graphics_card = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    cpu = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.name}"

# Quản lý các máy tính cụ thể:
class ComputerList(models.Model):
    name = models.CharField(max_length=100)
    computer_type = models.ForeignKey(ComputerType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return f"id:{self.id} {self.name} - Type: {self.computer_type.name} - {'Active' if self.is_active else 'Inactive'}"
    
# Quản lý các phiên sử dụng máy tính của người dùng:
class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pc = models.ForeignKey(ComputerList, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - Active: {self.is_active}"