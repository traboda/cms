from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def router_data(request):

    if request.method == "GET":
        return HttpResponse("Method not Allowed", content_type='text/plain', status=405)

    if request.method == "POST":
        from attendance.models import AttendanceLog, AttendanceDevice

        body = request.body.decode("utf-8")
        data = body.split('\n')

        logs = []
        print(len(data), 'mac IDs received')

        timestamp = timezone.datetime.strptime(data[0], '%m-%d-%H-%M')
        timestamp = timestamp.replace(year=timezone.now().year)
        print('Timestamp:', timestamp)

        for mac in data[1:]:
            try:
                device = AttendanceDevice.objects.get(macAddress__iexact=mac)
                logs.append(
                    AttendanceLog(
                        member=device.member,
                        device=device,
                        timestamp=timestamp
                    )
                )
            except AttendanceDevice.DoesNotExist:
                pass
        AttendanceLog.objects.bulk_create(logs, ignore_conflicts=True)
        return HttpResponse(status=200)
