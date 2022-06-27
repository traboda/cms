from uuid import uuid4

from django.conf import settings
from django.utils import timezone
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext, InlineQueryHandler,
)

from .bunkRequestHandler import BunkRequestHandler
from .adminCommandHandler import AdminCommandHandler


class GroupInlineQuery:

    def who_is_in_lab(self):
        from attendance.models import WiFiAttendanceLog
        logs = WiFiAttendanceLog.objects.filter(
            timestamp__gt=timezone.now() - timezone.timedelta(minutes=3),
        ).distinct('member')

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


class ChowkidarBot(BunkRequestHandler, AdminCommandHandler, GroupInlineQuery):

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
        dispatcher.add_handler(self.get_admin_commmand_handler())
        dispatcher.add_handler(self.get_bunk_handler())
        dispatcher.add_handler(self.get_scoot_handler())
        dispatcher.add_handler(self.get_leave_handler())
        dispatcher.add_handler(CommandHandler("tata", self.tata))
        dispatcher.add_handler(InlineQueryHandler(self.inline_query))

        updater.start_polling()

        updater.idle()
