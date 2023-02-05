from django.http import HttpResponse
from django.utils import timezone
from django.views import View

from api.utils.decorator import verify_API_key


class AttendanceLogAPI(View):

    @staticmethod
    @verify_API_key
    def post(request, *args, **kwargs):
        from attendance.models import AttendanceDevice, AttendanceDateLog, AttendanceTrackerLog

        if request.token.client.attendance < 2:
            print('invalid auth token permission')
            return HttpResponse("Permission Denied", content_type='text/plain', status=401)

        body = request.body.decode("utf-8")
        data = body.split('\n')

        logs = []

        timestamp = timezone.datetime.strptime(data[0], '%m-%d-%H-%M')
        timestamp = timestamp.replace(year=timezone.now().year)
        print('Timestamp:', timestamp)

        if AttendanceTrackerLog.objects.filter(timestamp=timestamp, client=request.token.client).exists():
            return HttpResponse(status=200)

        # convert mac addresses to uppercase
        for i in range(1, len(data)):
            data[i] = data[i].upper()

        devices = AttendanceDevice.objects.filter(macAddress__in=data[1:])

        AttendanceTrackerLog.objects.create(
            timestamp=timestamp,
            client=request.token.client,
            logs={
                'totalMacs': len(data) - 1,
                'macs': data[1:],
                'totalDevices': len(devices),
                'users': [
                    (d.member.username, d.macAddress) for d in devices
                ]
            }
        )

        timestring = timestamp.strftime('%H:%M')
        for device in devices:
            if AttendanceDateLog.objects.filter(member=device.member, date=timestamp.date()).exists():
                entry = AttendanceDateLog.objects.get(member=device.member, date=timestamp.date())
                if entry.logs is None:
                    entry.logs = {}

                if str(timestring) not in entry.logs:
                    entry.logs[timestring] = []
                entry.logs[timestring].append(device.macAddress)
                entry.lastSeen = timestring
                entry.save()
                member = device.member
            else:
                logs.append(
                    AttendanceDateLog(
                        member=device.member,
                        date=timestamp.date(),
                        logs={
                            timestring: [device.macAddress],
                        },
                        lastSeen=timestring
                    )
                )
                member = device.member
            member.lastSeen = timezone.now()
            member.save()
        AttendanceDateLog.objects.bulk_create(logs, ignore_conflicts=True)
        return HttpResponse(status=200)


__all__ = [
    'AttendanceLogAPI',
]
