from django.contrib import admin

from .models import AttendanceDevice, AttendanceLog, LeaveRequest, AttendanceTracker


@admin.register(AttendanceLog)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member', 'device', 'timestamp']
    list_filter = ['timestamp']


@admin.register(AttendanceDevice)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'member', 'macAddress']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['member', 'category', 'timestamp']
    list_filter = ['category', 'timestamp']


@admin.register(AttendanceTracker)
class AttendanceTrackerAdmin(admin.ModelAdmin):
    list_display = ['type', 'api_key', 'timestamp']
    list_filter = ['type']
