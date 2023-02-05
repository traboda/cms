from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from api.utils.decorator import verify_API_key
from attendance.models import AttendanceDateLog


class AttendanceProfileAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, userID, *args, **kwargs):
        from membership.models import Member
        try:
            member = Member.objects.get(id=userID)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member does not exist.'}, status=404)

        data = {}
        data['member'] = {
            'id': member.id,
            'name': member.name,
            'group': member.group.name if member.group else None
        }
        data['lastSeen'] = member.lastSeen.astimezone(timezone.get_current_timezone()).isoformat()
        now = timezone.now().astimezone(timezone.get_current_timezone())

        presenceLast7Days = AttendanceDateLog.objects.filter(
            member=member,
            date__gte=(now - timezone.timedelta(days=7)).date()
        ).count()
        presenceLast30Days = AttendanceDateLog.objects.filter(
            member=member,
            date__gte=(now - timezone.timedelta(days=30)).date()
        ).count()
        presenceLast6Months = AttendanceDateLog.objects.filter(
            member=member,
            date__gte=(now - timezone.timedelta(days=30 * 6)).date()
        ).count()

        data['stats'] = {
            'presence': {
               'last7Days': presenceLast30Days,
               'last30Days': presenceLast30Days,
               'last6Months': presenceLast6Months,
            },
            'absence': {
                'last7days': 7 - presenceLast7Days,
                'last30days': 30 - presenceLast30Days,
                'last6Months': 30 * 6 - presenceLast6Months,
            }
        }

        data['thisWeek'] = {
            'range': {
                'start': (now - timezone.timedelta(days=7)).date().isoformat(),
                'end': now.date().isoformat()
            },
        }
        # loop from today back to same day last week, and make an object with name of day and minutes
        for i in range(8):
            day = (now - timezone.timedelta(days=i)).date()
            try:
                log = AttendanceDateLog.objects.get(member=member, date=day)
                firstSeen = log.firstSeenTime()
                lastSeen = log.lastSeenTime()
                data['thisWeek'][day.isoformat()] = {
                    'day': day.strftime('%A'),
                    'minutes': log.minutes,
                    'firstSeen': firstSeen.strftime('%I:%M%p') if firstSeen else None,
                    'lastSeen': lastSeen.strftime('%I:%M%p') if lastSeen else None,
                    'sessions': log.find_sessions_from_logs()
                }
            except AttendanceDateLog.DoesNotExist:
                pass

        data['thisMonth'] = {
            'range': {
                'start': (now - timezone.timedelta(days=30)).date().isoformat(),
                'end': now.date().isoformat()
            },
            'stats': {},
            'logs': {}
        }
        totalMinutes = 0
        firstSeenTimes = []
        lastSeenTimes = []
        countedDays = 0
        for i in range(30):
            day = (now - timezone.timedelta(days=i)).date()
            try:
                log = AttendanceDateLog.objects.get(member=member, date=day)
                firstSeen = log.firstSeenTime()
                lastSeen = log.lastSeenTime()
                data['thisMonth']['logs'][day.isoformat()] = log.minutes
                firstSeenTimes.append(firstSeen.strftime('%I:%M%p'))
                lastSeenTimes.append(lastSeen.strftime('%I:%M%p'))
                totalMinutes += log.minutes
                countedDays += 1
            except AttendanceDateLog.DoesNotExist:
                pass
        data['thisMonth']['stats'] = {
            'totalMinutes': totalMinutes,
            'averageMinutes': round(totalMinutes / countedDays) if countedDays > 0 else 0,
        }
        return JsonResponse(data, status=200)


__all__ = [
    'AttendanceProfileAPI'
]
