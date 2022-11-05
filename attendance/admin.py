from django.contrib import admin

from .models import AttendanceDevice, AttendanceLog, LeaveRequest, AttendanceDateLog


@admin.register(AttendanceDateLog)
class AttendanceDateLogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['member', 'date', 'minutes']
    search_fields = ['member__name', 'member__email', 'member__id', 'date']
    list_filter = ['date']


@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member', 'device']
    search_fields = ['member', 'device__macAddress', 'tracker']
    list_display = ['member', 'type', 'device', 'timestamp', 'tracker']
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
