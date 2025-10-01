from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import *

# Đăng ký Menu bình thường
admin.site.register(Menu)
admin.site.register(Session)
admin.site.register(ComputerType)
admin.site.register(ComputerList)

# Đăng ký User với UserAdmin tuỳ biến, bao gồm các trường bổ sung và mã hoá mật khẩu khi tạo tài khoản trên admin
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Extra info', {'fields': ('phone_number', 'money_left')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Extra info', {'fields': ('phone_number', 'money_left')}),
    )
