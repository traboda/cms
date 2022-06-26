from django.contrib import admin

from .models import Member, Group


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username']


@admin.register(Group)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name']

