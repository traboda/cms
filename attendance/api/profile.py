from django.db.models import Sum, Avg
from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from api.utils.decorator import verify_API_key
from attendance.models import AttendanceDateLog

DEFAULT_DATE = timezone.datetime(2022, 11, 27, tzinfo=timezone.get_current_timezone())


def get_latest_date(offsetDays: int, dateJoined):
    offsetDate = timezone.now().astimezone(timezone.get_current_timezone()) - timezone.timedelta(days=offsetDays)
    if offsetDate.date() < dateJoined:
        return (timezone.now().astimezone(timezone.get_current_timezone()).date() - dateJoined).total_seconds() / 86400
    return offsetDays


class AttendanceProfileAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, userID, *args, **kwargs):
        from membership.models import Member
        try:
            member = Member.objects.get(id=userID)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member does not exist.'}, status=404)

        dateJoined = member.joinDate if member.joinDate else DEFAULT_DATE

        data = {}
        data['member'] = {
            'id': member.id,
            'name': member.name,
            'dateJoined': dateJoined,
            'group': member.group.name if member.group else None
        }
        data['lastSeen'] = (
            member.lastSeen.astimezone(timezone.get_current_timezone()).isoformat()
        ) if member.lastSeen else None
        now = timezone.now().astimezone(timezone.get_current_timezone())

        presenceLast7Days = AttendanceDateLog.objects.filter(
            member=member,
            date__gte=(now - timezone.timedelta(days=6)).date()
        )
        presenceLast30Days = AttendanceDateLog.objects.filter(
            member=member,
            date__gte=(now - timezone.timedelta(days=30-1)).date()
        )
        presenceLast6Months = AttendanceDateLog.objects.filter(
            member=member,
            date__gte=(now - timezone.timedelta(days=(30 * 6)-1)).date()
        )

        presenceLast6MonthsCount = presenceLast6Months.count()
        presenceLast30DaysCount = presenceLast30Days.count()
        presenceLast7DaysCount = presenceLast7Days.count()
        last7DaysAvg = presenceLast7Days.aggregate(avg=Avg('duration'))['avg'] or timezone.timedelta(seconds=0)
        last30DaysAvg = presenceLast30Days.aggregate(avg=Avg('duration'))['avg'] or timezone.timedelta(seconds=0)
        last6MonthsAvg = presenceLast6Months.aggregate(avg=Avg('duration'))['avg'] or timezone.timedelta(seconds=0)
        data['stats'] = {
            'presence': {
               'last7Days': presenceLast7DaysCount,
               'last30Days': presenceLast30DaysCount,
               'last6Months': presenceLast6MonthsCount,
            },
            'absence': {
                'last7Days': get_latest_date(7, dateJoined) - presenceLast7DaysCount,
                'last30Days': get_latest_date(30, dateJoined) - presenceLast30DaysCount,
                'last6Months': get_latest_date((30 * 6)-1, dateJoined) - presenceLast6MonthsCount,
            },
            'avgDuration': {
                'last7Days': last7DaysAvg.total_seconds() // 60,
                'last30Days': last30DaysAvg.total_seconds() // 60,
                'last6Months': last6MonthsAvg.total_seconds() // 60,
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
        data['attendanceCalendar'] = {}
        logs = AttendanceDateLog.objects.filter(member=member).order_by('date').only('date', 'duration')
        for log in logs:
            data['attendanceCalendar'][log.date.isoformat()] = round(log.duration.total_seconds() / 60)
        return JsonResponse(data, status=200)


__all__ = [
    'AttendanceProfileAPI'
]
