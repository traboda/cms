from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def log_sniffed_mac(request):

    if request.method == "GET":
        return HttpResponse("Method Not Allowed", content_type='text/plain', status=405)

    if request.method == "POST":
        from attendance.models import AttendanceDevice, AttendanceDateLog

        auth_token = request.headers.get('Authorization')

        if auth_token is None:
            return HttpResponse("Unauthorized", content_type='text/plain', status=401)

        from api.models import APIToken
        if auth_token.split(' ')[0] != 'Bearer':
            return HttpResponse("Unauthorized", content_type='text/plain', status=401)
        auth_token = auth_token.split(' ')[1]

        try:
            token = APIToken.objects.get(token=auth_token)
        except APIToken.DoesNotExist:
            return HttpResponse("Invalid Token", content_type='text/plain', status=401)

        if token.client.attendance < 2:
            return HttpResponse("Permission Denied", content_type='text/plain', status=401)

        body = request.body.decode("utf-8")
        data = body.split('\n')

        logs = []
        print(len(data), 'mac IDs received')

        timestamp = timezone.datetime.strptime(data[0], '%m-%d-%H-%M')
        timestamp = timestamp.replace(year=timezone.now().year)
        print('Timestamp:', timestamp)

        devices = AttendanceDevice.objects.filter(macAddress__iregex=r'(' + '|'.join(data[1:]) + ')')
        for device in devices:
            log = {
                'type': 'WIFI_SNIFFING',
                'device': {
                    'id': device.id,
                    'name': device.name,
                },
                'timestamp': timestamp,
                'tracker': token.client.name,
            }
            if AttendanceDateLog.objects.filter(member=device.member, date=timestamp.date()).exists():
                entry = AttendanceDateLog.objects.get(member=device.member, date=timestamp.date())
                entry.minutes += 5
                if entry.logs is None:
                    entry.logs = []
                entry.logs.append(log)
                entry.save()
            else:
                logs.append(
                    AttendanceDateLog(
                        member=device.member,
                        date=timestamp.date(),
                        minutes=5,
                        logs=[log]
                    )
                )
        AttendanceDateLog.objects.bulk_create(logs, ignore_conflicts=True)
        return HttpResponse(status=200)


__all__ = [
    'log_sniffed_mac',
]
