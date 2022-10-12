from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def router_data(request):

    if request.method == "GET":
        return HttpResponse("Method not Allowed", content_type='text/plain', status=405)

    if request.method == "POST":
        from attendance.models import AttendanceLog, AttendanceDevice
        body = request.body.decode("utf-8")
        data = body.split('\n')
        for client in data[1:]:
            try:
                device = AttendanceDevice.objects.get(macAddress=client)
                AttendanceLog.objects.create(
                    member=device.member,
                    device=device
                )
            except AttendanceDevice.DoesNotExist:
                pass

        return HttpResponse(status=200)
