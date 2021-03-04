from django.contrib import admin
from .models import Post, Like


# Register your models here.


@admin.register(Post)
class TaskAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Post._meta.fields]


@admin.register(Like)
class TaskAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Like._meta.fields]
