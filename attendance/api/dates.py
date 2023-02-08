from django.db.models import Count
from django.http import JsonResponse
from django.views import View

from api.utils.decorator import verify_API_key
from attendance.models import AttendanceDateLog


class AttendanceDatesAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, *args, **kwargs):
        logs = AttendanceDateLog.objects.only('date').values('date').annotate(count=Count('date'))
        data = {}
        for log in logs:
            data[log['date'].isoformat()] = log['count']
        return JsonResponse(data, status=200)


__all__ = [
    'AttendanceDatesAPI'
]
