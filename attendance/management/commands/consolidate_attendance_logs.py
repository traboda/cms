from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'cleans up attendance logs'

    def handle(self, *args, **options):
        from attendance.models import AttendanceLog, AttendanceDateLog

        logs = AttendanceLog.objects.all()
        for log in logs:
            date = log.timestamp.date()
            if AttendanceDateLog.objects.filter(member=log.member, date=date).exists():
                attendance_date_log = AttendanceDateLog.objects.get(member=log.member, date=date)
                attendance_date_log.minutes += 5
                attendance_date_log.logs.append(log.data)
                attendance_date_log.save()
            else:
                AttendanceDateLog.objects.create(
                    member=log.member,
                    date=date,
                    minutes=5,
                    logs=[log.data]
                )
            log.delete()

