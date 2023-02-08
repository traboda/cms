from django.contrib import admin

from .models import Member, Group, Hostel, SpecialDate, Team


@admin.register(Hostel)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(SpecialDate)
class SpecialDateAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username']
    list_display = ['name', 'team', 'batch', 'hostel']
    list_editable = ['hostel', 'team', 'batch']
    autocomplete_fields = ['group', 'hostel']
    list_filter = ['group', 'isActive', 'hostel', 'gender', 'batch', 'team']


@admin.register(Group)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Team)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
