from django.conf import settings
from django.utils import timezone
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext, MessageHandler, Filters
)


def day_beginning(dt=None):
    if not dt:
        dt = timezone.now()

    return timezone.localtime(dt).replace(hour=0, minute=0, second=0, microsecond=0)

# Testing has not been done for this one yet.
# Would require data for users and other things to be in database for testing it.
# Separate test case testing is avoided for now.
# Incomplete Implementation.
class GiveStayBacks:

    def checkForEligibility(self, member) -> bool:
        from attendance.models import AttendanceLog
        if not AttendanceLog.objects.filter(member=member, date=timezone.now().date()).exists():
            return False
        return True

    def getLastSeen(self, update: Update, context: CallbackContext):
        from attendance.models import AttendanceLog

        attendance_log = AttendanceLog.objects.filter(timestamp__gt=day_beginning()).order_by('-timestamp')
        # update.message.reply_text(f"{attendance_log[0].member.name} was last seen {attendance_log[0].timestamp}")
        attendance_log.filter(member=update.message.from_user.id).update(last_seen=timezone.now())
        # update.message.reply_text(f"{attendance_log.__dict__}")
        if not attendance_log.exists():
            update.message.reply_text("Hmm it seems, so far, no one came here today. :/")
            return ConversationHandler.END

        all_present_today = "Ok, here are the people who came today:\n"
        index = 1
        for attendance in attendance_log:
            member = attendance.member
            if self.checkForEligibility(member):
                all_present_today += f"  {index}. {member}  Last seen at: {attendance.timestamp}\n"
                index += 1
        update.message.reply_text(all_present_today)
        return ConversationHandler.END
