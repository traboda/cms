from django.utils import timezone
from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackContext, MessageHandler, Filters,
)

BUNK_CAT, BUNK_EXP, BUNK_CANCEL = map(chr, range(3))


class LeaveRequestHandler:

    def request_bunk(self, update: Update, context: CallbackContext):
        from membership.models import Member
        try:
            user = Member.objects.get(telegramID=update.message.from_user.id)
            context.user_data['user'] = user
        except Member.DoesNotExist:
            update.message.reply_text('I could not recognize you. My boss insists I dont talk to strangers.')
            return ConversationHandler.END

        group = user.group

        if not group:
            update.message.reply_text("You dont belong to any  groups. You don't need leaves :) ")
            return ConversationHandler.END

        if not group.is_working_today():
            update.message.reply_text('Today is anyway a holiday. Chill')
            return ConversationHandler.END

        if update.message.text == "/scoot":
            if not group.is_scootable():
                update.message.reply_text("You cannot scoot now")
                return ConversationHandler.END
            context.user_data['type'] = "SCOOT"
        elif update.message.text == "/bunk":
            if not group.is_bunkable():
                update.message.reply_text("You cannot bunk now")
                return ConversationHandler.END
            context.user_data['type'] = "BUNK"
        else:
            if not group.can_take_leave():
                update.message.reply_text("You cannot request a leave now. Try bunking or scooting!!")
                return ConversationHandler.END
            context.user_data['type'] = "LEAVE"

        from attendance.models import LeaveRequest

        if LeaveRequest.objects.filter(member=user, date=timezone.now().date()).exists():
            leave = LeaveRequest.objects.get(member=user, date=timezone.now().date())

            if context.user_data['type'] == "BUNK" and group.is_double_bunk():
                leave.type = "DOUBLE_BUNK"
            elif context.user_data['type'] == "SCOOT" and group.is_double_scoot():
                leave.type = "DOUBLE_SCOOT"

            leave.save()

            update.message.reply_text(
                "You already told me you are not coming today. I got it. Don't worry :)"
            )

            return ConversationHandler.END

        reply_keyboard = [
            ['I am a Student! 👨‍🎓', ],
            ['Getting Old 🤒', ],
            ['🎉 Pawri 💥 Ho Rahi 🎊 Hai ⚡️', ],
            ['Eyes are Red! 🥱😴'],
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
            type=context.user_data['type'],
            category=context.user_data['category'],
            description=context.user_data['description'],
        )
        return ConversationHandler.END

    def cancel_bunk(self, update: Update, context: CallbackContext) -> int:

        if update.message.text == "/cancelScoot":
            context.user_data['type'] = "SCOOT"
        elif update.message.text == "/cancelBunk":
            context.user_data['type'] = "BUNK"
        else:
            context.user_data['type'] = "LEAVE"

        from attendance.models import LeaveRequest
        if LeaveRequest.objects.filter(member__telegramID=update.message.from_user.id, date=timezone.now().date()).exists():
            leave = LeaveRequest.objects.get(member__telegramID=update.message.from_user.id, date=timezone.now().date())
            leave.delete()
            update.message.reply_text('That is better. See you at the lab!', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        update.message.reply_text("You have not applied for any")
        return ConversationHandler.END

    def get_leave_request_handler(self):
        return ConversationHandler(
            entry_points=[
                CommandHandler('bunk', self.request_bunk),
                CommandHandler('cancelBunk', self.cancel_bunk),
                CommandHandler('scoot', self.request_bunk),
                CommandHandler('cancelScoot', self.cancel_bunk),
                CommandHandler('leave', self.request_bunk),
                CommandHandler('cancelLeave', self.cancel_bunk),
            ],
            states={
                BUNK_CAT: [
                    MessageHandler(Filters.text, self.explain_bunk)
                ],
                BUNK_EXP: [MessageHandler(Filters.text, self.log_bunk)],
                BUNK_CANCEL: [
                    MessageHandler(Filters.text, self.cancel_bunk)
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel_bunk)],
        )