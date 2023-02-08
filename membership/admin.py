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
    list_display = ['name', 'group', 'team', 'isActive', 'graduationYear', 'hostel', 'gender']
    list_editable = ['gender', 'hostel', 'team', 'graduationYear', 'group']
    autocomplete_fields = ['group', 'hostel']
    list_filter = ['group', 'isActive', 'hostel', 'gender', 'graduationYear', 'team']


@admin.register(Group)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Team)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
