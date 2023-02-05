from django.urls import path

from .log_mac import AttendanceLogAPI
from .status import LiveAttendanceAPI

attendance_apis = [
    path('log', AttendanceLogAPI.as_view()),
    path('status', LiveAttendanceAPI.as_view()),
]

__all__ = [
    'attendance_apis',
]
