from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin 


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'age', 'phone', 'first_name', 'last_name']
    search_fields = ['username', 'phone', 'first_name', 'last_name',]

