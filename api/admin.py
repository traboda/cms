from django.contrib import admin
from .models import APIClient, APIToken


@admin.register(APIClient)
class APIClientAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'attendance', 'members']


@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    search_fields = ['token', 'client__name']
    list_display = ['client', 'token']
    autocomplete_fields = ['client']
    readonly_fields = ['token']
