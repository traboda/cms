from typing import List

from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from api.utils.decorator import verify_API_key
from attendance.models import AttendanceDateLog
from membership.models import Member


class LiveAttendanceAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, groupID=None, genderID=None, *args, **kwargs):
        now = timezone.now().astimezone(timezone.get_current_timezone())

        logQS = AttendanceDateLog.objects.all()
        memberQS = Member.objects.filter(isActive=True, exitDate__isnull=True)
        if groupID is not None:
            memberQS = memberQS.filter(group__id=groupID)
            logQS = logQS.filter(member__group__id=groupID)
        if genderID is not None:
            memberQS = memberQS.filter(gender=genderID)
            logQS = logQS.filter(member__gender=genderID)

        attendance = logQS.filter(
            date=now.date(),
            lastSeen__hour__gte=now.hour,
            lastSeen__minute__gte=now.minute - 10,
        )

        presentNowMemberIDs: List[int] = attendance.values_list('member_id', flat=True)
        presentTodayMemberIDs: List[int] = logQS.filter(
            date=now.date()
        ).values_list('member_id', flat=True)

        absentNowMemberIDs: List[int] = []
        for memberID in presentTodayMemberIDs:
            if memberID not in presentNowMemberIDs:
                absentNowMemberIDs.append(memberID)

        absentTodayMemberIDs: List[int] = memberQS.exclude(
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

        for member in memberQS.filter(id__in=presentNowMemberIDs, isActive=True):
            d = {
                'id': member.id,
                'name': member.name,
                'totalMinutes': attendance.get(member=member).minutes,
            }
            if groupID is None:
                d["group"] = {'id': member.group.id, 'name': member.group.name} if member.group else None
            data['now']['present'].append(d)

        for member in memberQS.filter(id__in=absentNowMemberIDs, isActive=True):
            d = {
                'id': member.id,
                'name': member.name,
                'totalMinutes': logQS.get(member=member, date=now.date()).minutes,
                'lastSeen': member.lastSeen.astimezone(
                    timezone.get_current_timezone()
                ).isoformat() if member.lastSeen else None,
            }
            if groupID is None:
                d["group"] = {'id': member.group.id, 'name': member.group.name} if member.group else None
            data['now']['absent'].append(d)

        for member in memberQS.filter(id__in=presentTodayMemberIDs).filter(isActive=True):
            d = {
                'id': member.id,
                'name': member.name,
                'group': {
                    'id': member.group.id,
                    'name': member.group.name,
                } if member.group else None,
                'totalMinutes': logQS.get(member=member, date=now.date()).minutes,
                'lastSeen': member.lastSeen.astimezone(
                    timezone.get_current_timezone()
                ).isoformat() if member.lastSeen else None,
            }
            if groupID is None:
                d["group"] = {'id': member.group.id, 'name': member.group.name} if member.group else None
            data['today']['present'].append(d)

        for member in memberQS.filter(id__in=absentTodayMemberIDs).filter(isActive=True):
            d = {
                'id': member.id,
                'name': member.name,
                'lastSeen': member.lastSeen.astimezone(
                    timezone.get_current_timezone()
                ).isoformat() if member.lastSeen else None,
            }
            if groupID is None:
                d["group"] = {'id': member.group.id, 'name': member.group.name} if member.group else None
            data['today']['absent'].append(d)

        return JsonResponse(data, status=200)


__all__ = [
    'LiveAttendanceAPI'
]
