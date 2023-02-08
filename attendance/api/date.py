from django.db.models import Avg
from django.http import JsonResponse
from django.views import View

from api.utils.decorator import verify_API_key
from attendance.models import AttendanceDateLog
from membership.models import Member, Group


class AttendanceDateSummaryAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, date, groupID = None, genderID = None, *args, **kwargs):
        logs = AttendanceDateLog.objects.filter(date=date)
        members = Member.objects.filter(isActive=True, joinDate__lte=date)

        data = {}
        data['date'] = date

        if groupID is not None:
            logs = logs.filter(member__group__id=groupID)
            members = members.filter(group__id=groupID)
            group = Group.objects.get(id=groupID)
            data['group'] = {
                'id': group.id,
                'name': group.name,
            }
        if genderID is not None:
            logs = logs.filter(member__gender=genderID)
            members = members.filter(gender=genderID)
            data['gender'] = {
                'id': genderID,
                'name': 'Male' if genderID is 1 else 'Female'
            }

        data['totalMembers'] = members.count()
        presentCount = logs.count()
        data['stats'] = {
            'present': presentCount,
            'absent': data['totalMembers'] - presentCount,
            'avgDuration': (
               logs.aggregate(avgDuration=Avg('duration'))['avgDuration'].total_seconds() / 60
               if presentCount > 0 else 0
            ),
        }
        top10Present = logs.order_by('-duration')[:10]
        data['stats']['topPresent'] = []
        for log in top10Present:
            data['stats']['topPresent'].append({
                'memberID': log.member.id,
                'name': log.member.name,
                'duration': log.duration.total_seconds() / 60,
            })
        if groupID is None:
            groups = Group.objects.all()
            data['groups'] = {}
            for group in groups:
                totalGroupMembers = members.filter(group=group).count()
                presentCount = logs.filter(member__group=group).count()
                data['groups'][group.name] = {
                    'total': totalGroupMembers,
                    'present': presentCount,
                    'absent': totalGroupMembers - presentCount,
                    'avgDuration': (
                        logs.filter(member__group=group).aggregate(avgDur=Avg('duration'))['avgDur'].total_seconds() / 60
                        if presentCount > 0 else 0
                    )
                }
        if genderID is None:
            data['gender'] = {}
            for i in ['M', 'F']:
                totalGenderMembers = members.filter(gender=1 if i == 'M' else 2).count()
                presentCount = logs.filter(member__gender=1 if i == 'M' else 2).count()
                data['gender'][i] = {
                    'total': totalGenderMembers,
                    'present': presentCount,
                    'absent': totalGenderMembers - presentCount,
                    'avgDuration': (
                        logs.filter(
                            member__gender=1 if i == 'M' else 2
                        ).aggregate(avgDur=Avg('duration'))['avgDur'].total_seconds() / 60
                        if presentCount > 0 else 0
                    )
                }

        if groupID is not None or genderID is not None:
            data['members'] = {
                'present': [],
                'absent': [],
            }
            for member in members:
                log = logs.filter(member=member).first()
                baseData = {
                    'id': member.id,
                    'name': member.name,
                }
                if groupID is None:
                    baseData['group'] = member.group.name if member.group else None
                if genderID is None:
                    baseData['gender'] = 'M' if member.gender == 1 else 'F'
                if log is not None:
                    data['members']['present'].append({
                        **baseData,
                        'totalMinutes': log.minutes if log is not None else 0,
                        'firstSeen': log.firstSeenTime().strftime("%I:%M%p") if log is not None else None,
                        'lastSeen': log.lastSeenTime().strftime("%I:%M%p") if log is not None else None,
                    })
                else:
                    data['members']['absent'].append(baseData)

        return JsonResponse(data, status=200)


__all__ = [
    'AttendanceDateSummaryAPI'
]
