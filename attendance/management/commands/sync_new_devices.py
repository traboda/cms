from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Sync new devices after they are added to the database'

    def handle(self, *args, **options):
        from attendance.models import AttendanceDevice, AttendanceTrackerLog, AttendanceDateLog

        logs = AttendanceTrackerLog.objects.all()
        for log in logs:
            timestamp = log.timestamp
            timestring = timestamp.strftime('%H:%M')
            macs = log.logs['macs']
            alreadyAddedMacs = []
            for m in log.logs['users']:
                alreadyAddedMacs.append(m[1])
            newMacs = list(set(macs) - set(alreadyAddedMacs))
            for mac in newMacs:
                if AttendanceDevice.objects.filter(macAddress=mac).exists():
                    device = AttendanceDevice.objects.get(macAddress=mac)
                    if AttendanceDateLog.objects.filter(member=device.member, date=timestamp.date()).exists():
                        entry = AttendanceDateLog.objects.get(member=device.member, date=timestamp.date())
                        if entry.logs is None:
                            entry.logs = {}

                        if str(timestring) not in entry.logs:
                            entry.logs[timestring] = []
                        if device.macAddress not in entry.logs[timestring]:
                            entry.logs[timestring].append(device.macAddress)
                            entry.lastSeen = timestring
                            entry.save()
                            print('updated for', device.member.username)
                    else:
                        AttendanceDateLog.objects.create(
                            member=device.member,
                            date=timestamp.date(),
                            logs={
                                timestring: [device.macAddress],
                            },
                            lastSeen=timestring
                        )
                        print('added for', device.member.username)
