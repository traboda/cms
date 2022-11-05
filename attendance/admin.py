from django.contrib import admin

from .models import AttendanceDevice, AttendanceLog, LeaveRequest


@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member', 'device']
    search_fields = ['member', 'device__macAddress']
    list_display = ['member', 'type', 'device', 'timestamp']
    list_filter = ['type', 'timestamp']


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
