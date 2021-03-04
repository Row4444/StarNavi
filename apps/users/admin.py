from django.contrib import admin
from .models import  User
# Register your models here.


@admin.register(User)
class TaskAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]