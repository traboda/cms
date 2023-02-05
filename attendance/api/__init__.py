from django.urls import path

from .log_mac import AttendanceLogAPI
from .profile import AttendanceProfileAPI
from .status import LiveAttendanceAPI
from .date import AttendanceDateSummaryAPI

attendance_apis = [
    path('log/', AttendanceLogAPI.as_view()),
    path('status/', LiveAttendanceAPI.as_view()),
    path('profile/<int:userID>/', AttendanceProfileAPI.as_view()),
    path('date/<str:date>/', AttendanceDateSummaryAPI.as_view()),
    path('date/<str:date>/group/<int:groupID>', AttendanceDateSummaryAPI.as_view()),
    path('date/<str:date>/gender/<int:genderID>', AttendanceDateSummaryAPI.as_view()),

]

__all__ = [
    'attendance_apis',
]
