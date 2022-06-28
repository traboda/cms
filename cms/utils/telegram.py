from uuid import uuid4

from django.conf import settings
from django.utils import timezone
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    InlineQueryHandler,
    CallbackContext,
)

BUNK_CAT, BUNK_EXP, BUNK_CANCEL = map(chr, range(3))

from .leaveRequestHandler import LeaveRequestHandler
from .adminCommandHandler import AdminCommandHandler


class LeaveRequestAppliedLister:

    def get_member(self, update, context):
        from membership.models import Member
        try:
            user = Member.objects.get(telegramID=update.message.from_user.id)
            context.user_data['user'] = user
            return user
        except Member.DoesNotExist:
            update.message.reply_text("I could not recognize you. My boss insists I don't talk to strangers.")
            return ConversationHandler.END

    def does_anyone_apply_for_leave(self, update, type_of_leave):
        from attendance.models import LeaveRequest
        if not LeaveRequest.objects.filter(date=timezone.now().date(), type=str(type_of_leave.upper())).exists():
            update.message.reply_text(f"No one has applied for any {type_of_leave} today. ;)")
            return False
        return True

    def list_requests(self, update: Update, context: CallbackContext):
        type_of_leave = update.message.text.split('_')[0][1:]
        from attendance.models import LeaveRequest

        if self.does_anyone_apply_for_leave(update, type_of_leave):
            output_str = f"Here are the {type_of_leave} requests for today:\n"
            index = 1
            for leave_request in LeaveRequest.objects.filter(date=timezone.now().date(), type=type_of_leave.upper()):
                output_str += f"  {index}. {leave_request.member.name}\n"
            update.message.reply_text(output_str)

        return ConversationHandler.END

    def show_vanish(self, update: Update, context: CallbackContext):
        from membership.models import Member
        from attendance.models import LeaveRequest, AttendanceLog

        lr = LeaveRequest.objects.filter(date=timezone.now().date())
        mlr = []

        for leave_request in lr:
            mlr.append(leave_request.member.id)

        aml = []

        al = AttendanceLog.objects.filter(timestamp__day=timezone.now().day).distinct('member')
        for attendance_log in al:
            aml.append(attendance_log.member.id)

        fml = Member.objects.exclude(id__in=mlr).exclude(id__in=aml).order_by('name')

        if fml.exists():
            output_str = f"Here are the people who vanished:\n"
            index = 1
            for member in fml:
                output_str += f"  {index}. {member.name}\n"
                index += 1

            update.message.reply_text(output_str)
        else:
            update.message.reply_text("No one has applied for vanish today. ;))")

        return ConversationHandler.END

    def show_leave_requests_handler(self):
        return ConversationHandler(
            entry_points=[
                CommandHandler('leave_requests', self.list_requests),
                CommandHandler('bunk_requests', self.list_requests),
                CommandHandler('scoot_requests', self.list_requests),
                CommandHandler('show_vanish', self.show_vanish),
            ],
            states={},
            fallbacks=[CommandHandler('cancel', ConversationHandler.END)],
        )


class GroupInlineQuery:

    def who_is_in_lab(self):
        from attendance.models import AttendanceLog
        logs = AttendanceLog.objects.filter(timestamp__gt=timezone.now() - timezone.timedelta(minutes=5),type='WIFI').distinct('member')
        if len(logs) == 0:
            return """
                **whoIsInLab**
                
                No one is in the lab right now.
            """
        msg = """
        **whoIsInLab**
        Alright, I can see the following people in lab \-
        """
        index = 0
        todayStart = timezone.now() - timezone.timedelta(hours=24)
        for l in logs:
            index += 1
            msg += f'{index}\. {l.member.name} \- {l.member.wifiattendancelog_set.filter(timestamp__gt=todayStart).count()} mins\n'
        return msg

    def inline_query(self, update: Update, context: CallbackContext):
        query = update.inline_query.query

        if not query or query == "":
            return

        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="whoBunked",
                input_message_content=InputTextMessageContent(
                    self.who_is_in_lab(),
                    parse_mode='MarkdownV2'
                ),
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="whoIsInLab",
                input_message_content=InputTextMessageContent(
                    self.who_is_in_lab(),
                    parse_mode='MarkdownV2'
                ),
            )
        ]

        update.inline_query.answer(results)


class ChowkidarBot(LeaveRequestHandler, LeaveRequestAppliedLister, AdminCommandHandler, GroupInlineQuery):

    def start(self, update: Update, context: CallbackContext):
        from membership.models import Member
        try:
            user = Member.objects.get(telegramID=update.message.from_user.id)
            return update.message.reply_text(f"Hello {user.name}!")
        except Member.DoesNotExist:
            update.message.reply_text(
                f"I could not recognize you. Please ask our admin to add you (id: {update.message.from_user.id}) to the system."
            )
            return ConversationHandler.END

    def who_is_in_lab_cmd(self, update: Update, context: CallbackContext):
        update.message.reply_text(self.who_is_in_lab())
        return ConversationHandler.END

    def tata(self, update: Update, context: CallbackContext):
        # add everything to daily and delete log
        if update.effective_chat.type == update.effective_chat.PRIVATE:
            update.message.reply_text("Your status update")

        else:
            update.message.reply_text("Please DM me", quote=True)

    def start_bot(self):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(self.admin_add_group_handler())
        dispatcher.add_handler(self.admin_add_user_handler())
        dispatcher.add_handler(self.admin_add_device_handler())
        dispatcher.add_handler(self.get_leave_request_handler())
        dispatcher.add_handler(self.show_leave_requests_handler())
        dispatcher.add_handler(CommandHandler("who_is_in_lab", self.who_is_in_lab_cmd))
        dispatcher.add_handler(CommandHandler("tata", self.tata))
        dispatcher.add_handler(InlineQueryHandler(self.inline_query))

        updater.start_polling()

        updater.idle()
