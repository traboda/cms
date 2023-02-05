from django.core.management import BaseCommand
from attendance.models import AttendanceDateLog
from membership.models import Member


class Command(BaseCommand):
    help = 'Update duration for logs'

    def handle(self, *args, **options):
        log = AttendanceDateLog.objects.all()
        for l in log:
            from django.utils import timezone
            minutes = len(l.logs if l.logs else {}) * 5
            l.duration = timezone.timedelta(minutes=minutes)
            l.save()
