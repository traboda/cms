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

        # convert mac addresses to uppercase
        for i in range(1, len(data)):
            data[i] = data[i].upper()

        devices = AttendanceDevice.objects.filter(macAddress__in=data[1:])

        AttendanceTrackerLog.objects.create(
            timestamp=timestamp,
            client=token.client,
            logs={
                'totalMacs': len(data) - 1,
                'macs': data[1:],
                'totalDevices': len(devices),
                'users': [
                    (d.member.username, d.macAddress) for d in devices
                ]
            }
        )

        for device in devices:
            log = {
                'type': 'WIFI_SNIFFING',
                'mac': device.macAddress,
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
                timestring = timestamp.strftime('%H:%M')
                if str(timestring) not in entry.logs:
                    entry.logs[timestring] = []
                entry.logs[timestring].append(log)
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
