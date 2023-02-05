from typing import List

from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from api.utils.decorator import verify_API_key
from attendance.models import AttendanceDateLog


class LiveAttendanceAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, *args, **kwargs):
        now = timezone.now().astimezone(timezone.get_current_timezone())
        attendance = AttendanceDateLog.objects.filter(
            date=now.date(),
            lastSeen__hour__gte=now.hour,
            lastSeen__minute__gte=now.minute - 10,
        )
        from membership.models import Member

        presentNowMemberIDs: List[int] = attendance.values_list('member_id', flat=True)
        presentTodayMemberIDs: List[int] = AttendanceDateLog.objects.filter(
            date=now.date()
        ).values_list('member_id', flat=True)

        absentNowMemberIDs: List[int] = []
        for memberID in presentTodayMemberIDs:
            if memberID not in presentNowMemberIDs:
                absentNowMemberIDs.append(memberID)

        absentTodayMemberIDs: List[int] = Member.objects.exclude(
            id__in=presentTodayMemberIDs
        ).filter(isActive=True).values_list('id', flat=True)

        data = {}
        data['timestamp'] = now.isoformat()
        data['stats'] = {
            'presentToday': len(presentTodayMemberIDs),
            'absentToday': len(absentTodayMemberIDs),
            'presentNow': len(presentNowMemberIDs),
            'absentNow': len(absentNowMemberIDs),
        }

        data['now'] = {
            'present': [],
            'absent': [],
        }
        data['today'] = {
            'present': [],
            'absent': [],
        }
        for member in Member.objects.filter(id__in=presentNowMemberIDs, isActive=True):
            data['now']['present'].append({
                'id': member.id,
                'name': member.name,
                'totalMinutes': attendance.get(member=member).minutes,
            })
        for member in Member.objects.filter(id__in=absentNowMemberIDs, isActive=True):
            data['now']['absent'].append({
                'id': member.id,
                'name': member.name,
                'totalMinutes': AttendanceDateLog.objects.get(member=member, date=now.date()).minutes,
                'lastSeen': member.lastSeen.astimezone(
                    timezone.get_current_timezone()
                ).isoformat() if member.lastSeen else None,
            })
        for member in Member.objects.filter(id__in=presentTodayMemberIDs).filter(isActive=True):
            data['today']['present'].append({
                'id': member.id,
                'name': member.name,
                'totalMinutes': AttendanceDateLog.objects.get(member=member, date=now.date()).minutes,
                'lastSeen': member.lastSeen.astimezone(
                    timezone.get_current_timezone()
                ).isoformat() if member.lastSeen else None,
            })
        for member in Member.objects.filter(id__in=absentTodayMemberIDs).filter(isActive=True):
            data['today']['absent'].append({
                'id': member.id,
                'name': member.name,
                'lastSeen': member.lastSeen.astimezone(
                    timezone.get_current_timezone()
                ).isoformat() if member.lastSeen else None,
            })
        return JsonResponse(data, status=200)


__all__ = [
    'LiveAttendanceAPI'
]
