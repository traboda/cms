from django.contrib import admin

from .models import AttendanceDevice, LeaveRequest, AttendanceDateLog


@admin.register(AttendanceDateLog)
class AttendanceDateLogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['member', 'date', 'minutes']
    search_fields = ['member__name', 'member__email', 'member__id', 'date']
    list_filter = ['date']


@admin.register(AttendanceDevice)
class AttendanceDeviceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    search_fields = ['name', 'macAddress']
    list_display = ['name', 'member', 'macAddress']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['member', 'category', 'timestamp']
    list_filter = ['category', 'timestamp']
