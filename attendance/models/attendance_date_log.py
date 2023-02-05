from django.db import models


class AttendanceDateLog(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    logs = models.JSONField()
    lastSeen = models.TimeField(null=True, blank=True)

    @property
    def minutes(self):
        return len(self.logs if self.logs else {}) * 5

    @property
    def lastSeenTimestamp(self):
        return self.lastSeenTime().isoformat()

    @property
    def formattedTime(self):
        totalMinutes = self.minutes
        hours = totalMinutes // 60
        minutes = totalMinutes % 60
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

    def lastSeenTime(self):
        if self.lastSeen is None:
            return None
        hours, minutes = self.lastSeen.hour, self.lastSeen.minute
        date = self.date
        from django.utils import timezone
        return timezone.datetime(
            date.year, date.month, date.day, hours, minutes, tzinfo=timezone.get_current_timezone()
        )

    def firstSeenTime(self):
        if self.logs is None:
            return None
        keys = list(self.logs.keys())
        if len(keys) == 0:
            return None

        # order keys by earliest time
        keys.sort()
        hours, minutes = keys[0].split(':')
        hours, minutes = int(hours), int(minutes)
        date = self.date
        from django.utils import timezone
        return timezone.datetime(
            date.year, date.month, date.day, hours, minutes, tzinfo=timezone.get_current_timezone()
        )

    def lastSeenTime(self):
        if self.logs is None:
            return None
        keys = list(self.logs.keys())
        if len(keys) == 0:
            return None

        # order keys by latest time
        keys.sort(reverse=True)
        hours, minutes = keys[0].split(':')
        hours, minutes = int(hours), int(minutes)
        date = self.date
        from django.utils import timezone
        return timezone.datetime(
            date.year, date.month, date.day, hours, minutes, tzinfo=timezone.get_current_timezone()
        )

    def find_sessions_from_logs(self):
        # find continous set of logs which are in intervals of 5 minutes, and put them into a list of sessions,
        # where each session has a start time and end time
        sessions = []
        if self.logs is None:
            return sessions
        keys = list(self.logs.keys())
        if len(keys) == 0:
            return sessions
        keys.sort()
        currentSession = None
        for key in keys:
            hours, minutes = key.split(':')
            hours, minutes = int(hours), int(minutes)
            date = self.date
            from django.utils import timezone
            time = timezone.datetime(
                date.year, date.month, date.day, hours, minutes, tzinfo=timezone.get_current_timezone()
            )
            if currentSession is None:
                currentSession = {
                    'start': time,
                    'end': time,
                    'duration': 5
                }
            else:
                if (time - currentSession['end']).total_seconds() == 5 * 60:
                    currentSession['end'] = time
                    currentSession['duration'] = (currentSession['end'] - currentSession['start']).total_seconds() / 60
                else:
                    sessions.append(currentSession)
                    currentSession = {
                        'start': time,
                        'end': time,
                        'duration': 5
                    }
        if currentSession is not None:
            sessions.append(currentSession)

        data = []
        for session in sessions:
            data.append([
                session['start'].strftime('%I:%M%p'),
                session['end'].strftime('%I:%M%p'),
                session['duration']
            ])

        data.sort(key=lambda x: x[0])
        return data

    class Meta:
        unique_together = [
            ('member', 'date')
        ]
        db_table = 'attendance_date_log'
        verbose_name_plural = "Attendance Date Logs"
        verbose_name = "Attendance Date Log"

    def __str__(self):
        return str(self.id)


__all__ = [
    'AttendanceDateLog',
]
