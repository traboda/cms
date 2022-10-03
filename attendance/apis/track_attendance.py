import json

from django.http import JsonResponse, HttpResponse
from django.views import View


class LogAttendanceAPI(View):

    @staticmethod
    def post(request, *args, **kwargs):
        body = request.body.decode('utf-8')
        data = None
        if body:
            if request.content_type == 'application/json':
                data = json.loads(body)
            else:
                return JsonResponse('Invalid request body content type', status=400)

        if data["api_key"] is None:
            return JsonResponse("API Key is required", status=400)

        if data["mac_address"] is None:
            return JsonResponse("MAC Address is required", status=400)

        try:
            from attendance.models import AttendanceTracker
            attendance_tracker = AttendanceTracker.objects.get(api_key=data["api_key"])
        except AttendanceTracker.DoesNotExist:
            return JsonResponse('Invalid API key', status=401)

        try:
            from attendance.models import AttendanceLog, AttendanceDevice
            device = AttendanceDevice.objects.get(macAddress=data["mac_address"])
            AttendanceLog.objects.create(
                member=device.member,
                type=attendance_tracker.type,
                device=device,
            )
        except AttendanceDevice.DoesNotExist:
            return JsonResponse('Invalid MAC address', status=400)
        return HttpResponse(status=200)


__all__ = [
    'LogAttendanceAPI'
]
