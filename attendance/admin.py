from django.contrib import admin

from .models import AttendanceDevice, LeaveRequest, AttendanceDateLog, AttendanceTrackerLog


# class LasListFilter(admin.SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = _('decade born')
#
#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'decade'
#
#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return (
#             ('80s', _('in the eighties')),
#             ('90s', _('in the nineties')),
#         )
#
#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         # Compare the requested value (either '80s' or '90s')
#         # to decide how to filter the queryset.
#         if self.value() == '80s':
#             return queryset.filter(
#                 birthday__gte=date(1980, 1, 1),
#                 birthday__lte=date(1989, 12, 31),
#             )
#         if self.value() == '90s':
#             return queryset.filter(
#                 birthday__gte=date(1990, 1, 1),
#                 birthday__lte=date(1999, 12, 31),
#             )


@admin.register(AttendanceDateLog)
class AttendanceDateLogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['member', 'date', 'lastSeen', 'formattedTime']
    search_fields = ['member__name', 'member__email', 'member__id', 'date']
    list_filter = ['date', 'member__group', 'member__gender']
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
