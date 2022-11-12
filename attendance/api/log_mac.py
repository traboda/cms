from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def log_sniffed_mac(request):

    if request.method == "GET":
        return HttpResponse("Method Not Allowed", content_type='text/plain', status=405)

    if request.method == "POST":
        from attendance.models import AttendanceDevice, AttendanceDateLog, AttendanceTrackerLog

        auth_token = request.headers.get('Authorization')

        if auth_token is None:
            print('No auth token')
            return HttpResponse("Unauthorized", content_type='text/plain', status=401)

        from api.models import APIToken
        if auth_token.split(' ')[0] != 'Bearer':
            print('invalid auth token pattern')
            return HttpResponse("Unauthorized", content_type='text/plain', status=401)
        auth_token = auth_token.split(' ')[1]

        try:
            token = APIToken.objects.get(token=auth_token)
        except APIToken.DoesNotExist:
            print('invalid auth token')
            return HttpResponse("Invalid Token", content_type='text/plain', status=401)

        if token.client.attendance < 2:
            print('invalid auth token permission')
            return HttpResponse("Permission Denied", content_type='text/plain', status=401)

        body = request.body.decode("utf-8")
        data = body.split('\n')

        logs = []

        timestamp = timezone.datetime.strptime(data[0], '%m-%d-%H-%M')
        timestamp = timestamp.replace(year=timezone.now().year)
        print('Timestamp:', timestamp)

        if AttendanceTrackerLog.objects.filter(timestamp=timestamp, client=token.client).exists():
            return HttpResponse(status=200)

        AttendanceTrackerLog.objects.create(
            timestamp=timestamp,
            client=token.client,
            logs=data
        )
        devices = AttendanceDevice.objects.filter(macAddress__iregex=r'(' + '|'.join(data[1:]) + ')')
        for device in devices:
            log = {
                'type': 'WIFI_SNIFFING',
                'device': {
                    'id': device.id,
                    'name': device.name,
                },
                'tracker': token.client.name,
            }
            if AttendanceDateLog.objects.filter(member=device.member, date=timestamp.date()).exists():
                entry = AttendanceDateLog.objects.get(member=device.member, date=timestamp.date())
                if entry.logs is None:
                    entry.logs = {}
                if str(timestamp.isoformat()) not in entry.logs:
                    entry.logs[str(timestamp.isoformat())] = []
                entry.logs[str(timestamp.isoformat())].append(log)
                entry.save()
            else:
                logs.append(
                    AttendanceDateLog(
                        member=device.member,
                        date=timestamp.date(),
                        logs={
                            timestamp.isoformat(): log,
                        }
                    )
                )
        AttendanceDateLog.objects.bulk_create(logs, ignore_conflicts=True)
        return HttpResponse(status=200)


__all__ = [
    'log_sniffed_mac',
]
