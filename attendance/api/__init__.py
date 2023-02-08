from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .dates import AttendanceDatesAPI
from .log_mac import AttendanceLogAPI
from .profile import AttendanceProfileAPI
from .live import LiveAttendanceAPI
from .date import AttendanceDateSummaryAPI
from .profiles import AttendanceProfilesAPI

attendance_apis = [
    path('log/', csrf_exempt(AttendanceLogAPI.as_view())),
    path('profiles/', AttendanceProfilesAPI.as_view()),
    path('profile/<int:userID>/', AttendanceProfileAPI.as_view()),
    path('live/', LiveAttendanceAPI.as_view()),
    path('live/group/<int:groupID>/', LiveAttendanceAPI.as_view()),
    path('live/gender/<int:genderID>/', LiveAttendanceAPI.as_view()),
    path('dates/', AttendanceDatesAPI.as_view()),
    path('date/<str:date>/', AttendanceDateSummaryAPI.as_view()),
    path('date/<str:date>/group/<int:groupID>', AttendanceDateSummaryAPI.as_view()),
    path('date/<str:date>/gender/<int:genderID>', AttendanceDateSummaryAPI.as_view()),

]

__all__ = [
    'attendance_apis',
]
