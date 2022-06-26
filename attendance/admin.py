from django.contrib import admin

from .models import WiFiAttendanceLog, WiFiAttendanceDevice, LeaveRequest


@admin.register(WiFiAttendanceLog)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member', 'device', 'timestamp']
    list_filter = ['timestamp']


@admin.register(WiFiAttendanceDevice)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'member', 'macAddress']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['member', 'category', 'timestamp']
    list_filter = ['category', 'timestamp']
