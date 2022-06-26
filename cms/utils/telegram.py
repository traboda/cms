from uuid import uuid4

from django.conf import settings
from django.utils import timezone
from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext, MessageHandler, Filters, InlineQueryHandler,
)

BUNK_CAT, BUNK_EXP, BUNK_CANCEL = map(chr, range(3))


class BunkRequestHandler:

    def request_bunk(self, update: Update, context: CallbackContext):
        from membership.models import Member
        try:
            user = Member.objects.get(telegramID=update.message.from_user.id)
            context.user_data['user'] = user
        except Member.DoesNotExist:
            update.message.reply_text('I could not recognize you. My boss insists I dont talk to strangers.')
            return ConversationHandler.END

        from attendance.models import LeaveRequest
        today = timezone.now().date().isoformat()
        if LeaveRequest.objects.filter(member=user, date=timezone.now().date()).exists():
            update.message.reply_text(
                "You already told me you are not coming today. I got it. Don't worry :)"
            )
            return ConversationHandler.END

        reply_keyboard = [
          ['I am a Student! 👨‍🎓',],
          ['Getting Old 🤒',],
          ['🎉 Pawri 💥 Ho Rahi 🎊 Hai ⚡️',],
          ['Eyes are Red! 🥱😴'],
          ['NVM. Just kidding.']
        ]
        update.message.reply_text(
            text="Oh well, so you don't want to come to lab today...",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
            )
        )
        return BUNK_CAT

    def explain_bunk(self, update: Update, context: CallbackContext):
        answer = update.message.text
        if answer == "I am a Student! 👨‍🎓":
            cat = 'ACADEMICS'
            m1 = 'Ok, so I guess you have some homework, assignment, quiz or an exam that is upcoming...'
            m2 = 'Am I right? Maybe, you should type it in few words.'
        elif answer == "Getting Old 🤒":
            cat = 'HEALTH'
            m1 = "Sorry to hear you're not feeling well. Your health and well-being is important to me."
            m2 = "I don't know, I am a bit worried, what's it? did you see a doctor? got a medicine? do you usually have this?"
        elif answer == "🎉 Pawri 💥 Ho Rahi 🎊 Hai ⚡️":
            cat = 'ENTERTAINMENT'
            m1 = "I am glad you took your break! Work Hard, Play Hard!"
            m2 = "So, what's the plan? What's cooking?"
        elif answer == "Eyes are Red! 🥱😴":
            cat = 'SLEEP'
            m1 = "Sleep is very important. You cannot work now, I understand."
            m2 = "I had told you to sleep properly... What went wrong yesterday?"
        else:
            return BUNK_CANCEL
        update.message.reply_text(m1, quote=True)
        update.message.reply_text(m2)
        context.user_data['category'] = cat
        return BUNK_EXP

    def log_bunk(self, update: Update, context: CallbackContext):
        context.user_data['description'] = update.message.text
        data = context.user_data
        msg = ''
        if data['category'] == 'ACADEMICS':
            msg = 'All the best, scholar! Will see you later at the lab...'
        elif data['category'] == 'HEALTH':
            msg = 'Take good care of yourself. You should be fine. Will meet later at the lab...'
        elif data['category'] == 'ENTERTAINMENT':
            msg = 'Enjoy your time! Have fun, make memories. Cya later at the lab...'
        elif data['category'] == 'SLEEP':
            msg = 'Take rest, sleep well. You will be recharged. Will cya at the lab...'
        update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())

        from attendance.models import LeaveRequest
        LeaveRequest.objects.create(
            member=context.user_data['user'],
            date=timezone.now().date(),
            category=context.user_data['category'],
            description=context.user_data['description'],
        )
        return ConversationHandler.END

    def cancel_bunk(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text('That is better. See you at the lab!', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    def get_bunk_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler('bunk', self.request_bunk)],
            states={
                BUNK_CAT: [
                    MessageHandler(Filters.text, self.explain_bunk)
                ],
                BUNK_EXP: [MessageHandler(Filters.text, self.log_bunk)],
                BUNK_CANCEL: [
                    CommandHandler('cancel', self.cancel_bunk)
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel_bunk)],
        )


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
        print(query)

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


class ChowkidarBot(BunkRequestHandler, GroupInlineQuery):

    def start(self, update: Update, context: CallbackContext):
        print(update.message.from_user.id)
        from membership.models import Member
        try:
            user = Member.objects.get(telegramID=update.message.from_user.id)
            return update.message.reply_text(f"Hello {user.name}!")
        except Member.DoesNotExist:
            update.message.reply_text(
                f"I could not recognize you. Please ask our admin to add you (id: {update.message.from_user.id}) to the system."
            )
            return ConversationHandler.END

    def scoot(self, update: Update, context: CallbackContext):
        update.message.reply_text("You are not a scoot")

    def start_bot(self):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(self.get_bunk_handler())
        dispatcher.add_handler(CommandHandler("scoot", self.scoot))
        dispatcher.add_handler(InlineQueryHandler(self.inline_query))

        updater.start_polling()

        updater.idle()
