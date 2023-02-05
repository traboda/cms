from django.contrib import admin

from .models import Member, Group, Hostel, SpecialDate


@admin.register(Hostel)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(SpecialDate)
class SpecialDateAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username']
    list_display = ['name', 'group', 'isActive', 'hostel', 'gender']
    list_editable = ['gender', 'hostel', 'group']
    autocomplete_fields = ['group', 'hostel']
    list_filter = ['group', 'isActive', 'hostel', 'gender']


@admin.register(Group)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name']


