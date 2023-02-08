from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views import View

from api.utils.decorator import verify_API_key
from attendance.models import AttendanceDateLog
from membership.models import Member


class AttendanceProfilesAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, *args, **kwargs):
        logs = AttendanceDateLog.objects.values('member').annotate(count=Count('member'))
        data = {}
        members = Member.objects.filter(id__in=logs.values_list('member', flat=True))
        for log in logs:
            data[log['member']] = log['count']
        membersList = []
        for member in members:
            membersList.append({
                'id': member.id,
                'name': member.name,
                'group': {
                    'id': member.group.id,
                    'name': member.group.name,
                },
                'gender': member.gender,
                'count': data[member.id],
            })
        return JsonResponse(membersList, status=200, safe=False)


__all__ = [
    'AttendanceProfilesAPI'
]
