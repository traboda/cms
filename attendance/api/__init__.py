from django.urls import path

from .log_mac import AttendanceLogAPI
from .profile import AttendanceProfileAPI
from .live import LiveAttendanceAPI
from .date import AttendanceDateSummaryAPI

attendance_apis = [
    path('log/', AttendanceLogAPI.as_view()),
    path('profile/<int:userID>/', AttendanceProfileAPI.as_view()),
    path('live/', LiveAttendanceAPI.as_view()),
    path('live/group/<int:groupID>/', LiveAttendanceAPI.as_view()),
    path('live/gender/<int:genderID>/', LiveAttendanceAPI.as_view()),
    path('date/<str:date>/', AttendanceDateSummaryAPI.as_view()),
    path('date/<str:date>/group/<int:groupID>', AttendanceDateSummaryAPI.as_view()),
    path('date/<str:date>/gender/<int:genderID>', AttendanceDateSummaryAPI.as_view()),

]

__all__ = [
    'attendance_apis',
]
