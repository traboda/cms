from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from api.api import auth_apis
from attendance.api import attendance_apis
from attendance.api.log_mac import AttendanceLogAPI
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('log/macs/sniffed/', csrf_exempt(AttendanceLogAPI.as_view())),
    path('attendance/', include(attendance_apis)),
    path('auth/', include(auth_apis)),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('api/', include(urlpatterns))
]
