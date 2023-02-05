from django.core.management import BaseCommand
from attendance.models import AttendanceDateLog
from membership.models import Member


class Command(BaseCommand):
    help = 'Runs our telegram bot'

    def handle(self, *args, **options):
        members = Member.objects.filter(isActive=True)
        for member in members:
            log = AttendanceDateLog.objects.filter(member=member).order_by('-id').first()
            if log:
                member.lastSeen = log.lastSeenTime()
                member.save()
