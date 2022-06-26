from django.contrib import admin

from .models import AttendanceDevice, AttendanceLog, LeaveRequest


@admin.register(AttendanceLog)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member', 'type', 'device', 'timestamp']
    list_filter = ['type', 'timestamp']


@admin.register(AttendanceDevice)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'member', 'macAddress']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['member', 'category', 'timestamp']
    list_filter = ['category', 'timestamp']
