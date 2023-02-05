from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'fixing last seen'

    def handle(self, *args, **options):
        from attendance.models import AttendanceDateLog
        logs = AttendanceDateLog.objects.all()
        for log in logs:
            if log.logs:
                maxEntry = max(log.logs.keys())
                if len(maxEntry) > 5:
                    logs = log.logs.copy()
                    del logs[maxEntry]
                    if len(logs) > 0:
                        maxEntry = max(logs.keys())
                    else:
                        maxEntry = None
                log.lastSeen = maxEntry
            data = {}
            logs = log.logs
            for key in logs.keys():
                macs = []
                if type(logs[key]) == list:
                    newKey = key
                    for l in logs[key]:
                        macs.append(l['mac'])
                elif type(logs[key]) == dict:
                    newKey = key.split('T')[1][:5]
                    macs.append(logs[key]['mac'])
                data[newKey] = macs
            log.logs = data
            log.save()

