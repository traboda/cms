
from django.contrib import admin

from .models import AttendanceDevice, LeaveRequest, AttendanceDateLog, AttendanceTrackerLog


class DurationListFilter(admin.SimpleListFilter):
    title = 'duration'

    parameter_name = 'duration'

    def lookups(self, request, model_admin):
        return (
            ('0', 'upto 1 hr'),
            ('1', '1 - 3 hrs'),
            ('3', '3 - 6 hrs'),
            ('6', '6 - 12 hrs'),
            ('12', 'more than 12 hrs'),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        if self.value() == '0':
            return queryset.filter(
                duration__gte=timezone.timedelta(minutes=0),
                duration__lte=timezone.timedelta(minutes=60),
            )
        if self.value() == '1':
            return queryset.filter(
                duration__gte=timezone.timedelta(minutes=60),
                duration__lte=timezone.timedelta(minutes=180),
            )
        if self.value() == '3':
            return queryset.filter(
                duration__gte=timezone.timedelta(minutes=180),
                duration__lte=timezone.timedelta(minutes=360),
            )
        if self.value() == '6':
            return queryset.filter(
                duration__gte=timezone.timedelta(minutes=360),
                duration__lte=timezone.timedelta(minutes=720),
            )
        if self.value() == '12':
            return queryset.filter(
                duration__gte=timezone.timedelta(minutes=720),
            )


@admin.register(AttendanceDateLog)
class AttendanceDateLogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['member', 'date', 'lastSeen', 'duration']
    search_fields = ['member__name', 'member__email', 'member__id', 'date']
    list_filter = ['date', 'member__group', 'member__gender', DurationListFilter]
    ordering = ['-date', '-lastSeen', 'member__name']


@admin.register(AttendanceDevice)
class AttendanceDeviceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    search_fields = ['name', 'macAddress']
    list_display = ['name', 'member', 'macAddress']
    list_filter = ['member__group']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['member', 'category', 'timestamp']
    list_filter = ['category', 'timestamp']


@admin.register(AttendanceTrackerLog)
class AttendanceTrackerLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'totalUsers', 'totalMacs']
    list_filter = ['timestamp']
