from uuid import uuid4

from django.conf import settings
from django.utils import timezone
from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackContext, MessageHandler, Filters
)

USER_NAME, USER_ID, USER_GROUP, USER_CANCEL = map(chr, range(4))
GROUP_NAME, GROUP_WST, GROUP_WCT, GROUP_HST, GROUP_HCT = map(chr, range(5))


def getTimeFromFormat(update: Update, time):
    from datetime import datetime
    try:
        return datetime.strptime(time, '%H:%M').time()
    except ValueError:
        update.message.reply_text("Invalid time format")
        return False


class AdminCommandHandler:

    def add_user(self, update: Update, context: CallbackContext):
        if (update.effective_chat.type == update.effective_chat.PRIVATE and
                str(update.message.from_user.id) == settings.ADMIN_ID):
            update.message.reply_text(text="Ok so what is the username?")
            return USER_NAME
        else:
            update.message.reply_text("Action is restricted to admin only")
            return ConversationHandler.END

    def user_name(self, update: Update, context: CallbackContext):
        answer = update.message.text
        context.user_data['name'] = answer
        update.message.reply_text("Ok so what is the telegramID?")
        return USER_ID

    def user_id(self, update: Update, context: CallbackContext):
        from membership.models import Group

        answer = update.message.text
        context.user_data['telegramID'] = answer

        group = Group.objects.all()
        reply_keyboard = [[group.name for group in group]]
        update.message.reply_text(
            text="Which group do you want to add the user to?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Group?'
            )
        )
        return USER_GROUP

    def user_group(self, update: Update, context: CallbackContext):

        answer = update.message.text

        from membership.models import Member, Group
        if not Group.objects.filter(name=answer).exists():
            update.message.reply_text("Group does not exists")
            return ConversationHandler.END

        context.user_data['group'] = answer

        Member.objects.create(
            telegramID=context.user_data['telegramID'],
            name=context.user_data['name'],
            joinDate=timezone.now(),
            group=Group.objects.get(name=context.user_data['group']),
        )
        update.message.reply_text("User added successfully", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    def add_group(self, update: Update, context: CallbackContext):
        if (update.effective_chat.type == update.effective_chat.PRIVATE and
                str(update.message.from_user.id) == settings.ADMIN_ID):
            update.message.reply_text(text="Ok so what is the group name?")
            return GROUP_NAME
        else:
            update.message.reply_text("Action is restricted to admin only")
            return ConversationHandler.END

    def group_name(self, update: Update, context: CallbackContext):
        answer = update.message.text
        context.user_data['name'] = answer
        from membership.models import Group
        if Group.objects.filter(name=answer).exists():
            update.message.reply_text("Group already exists")
            return ConversationHandler.END

        update.message.reply_text("Ok so when is the opening time for this group during working days? \n Format: HH:MM")
        return GROUP_WST

    def group_wst(self, update: Update, context: CallbackContext):
        answer = update.message.text

        if not getTimeFromFormat(update=update, time=answer):
            return ConversationHandler.END

        context.user_data['wct'] = getTimeFromFormat(update=update, time=answer)

        update.message.reply_text("Ok so when is the closing time for this group during working days? \n Format: HH:MM")
        return GROUP_WCT

    def group_wct(self, update: Update, context: CallbackContext):
        answer = update.message.text

        if not getTimeFromFormat(update=update, time=answer):
            return ConversationHandler.END

        context.user_data['wct'] = getTimeFromFormat(update=update, time=answer)

        update.message.reply_text("Ok so when is the opening time for this group during holidays? \n Format: HH:MM")
        return GROUP_HST

    def group_hst(self, update: Update, context: CallbackContext):
        answer = update.message.text

        if not getTimeFromFormat(update=update, time=answer):
            return ConversationHandler.END

        context.user_data['hst'] = getTimeFromFormat(update=update, time=answer)

        update.message.reply_text("Ok so when is the closing time for this group during holidays? \n Format: HH:MM")
        return GROUP_HCT

    def group_hct(self, update: Update, context: CallbackContext):
        answer = update.message.text

        if not getTimeFromFormat(update=update, time=answer):
            return ConversationHandler.END

        context.user_data['hct'] = getTimeFromFormat(update=update, time=answer)

        from membership.models import Group
        Group.objects.create(
            name=context.user_data['name'],
            workingDayOpenTime=context.user_data['wst'],
            workingDayCloseTime=context.user_data['wct'],
            holidayOpenTime=context.user_data['hst'],
            holidayCloseTime=context.user_data['hct'],
        )
        update.message.reply_text("Group created successfully", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    def cancel_interaction(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(text="Interaction cancelled", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    def get_admin_commmand_handler(self):
        return ConversationHandler(
            entry_points=[
                CommandHandler('add_user', self.add_user),
                CommandHandler('add_group', self.add_group),
                CommandHandler('add_day_exception', self.add_user),
            ],
            states={
                USER_NAME: [
                    MessageHandler(Filters.text, self.user_name)
                ],
                USER_ID: [
                    MessageHandler(Filters.text, self.user_id)
                ],
                USER_GROUP: [
                    MessageHandler(Filters.text, self.user_group)
                ],
                USER_CANCEL: [
                    MessageHandler(Filters.text, self.cancel_interaction)
                ],
                GROUP_NAME: [
                    MessageHandler(Filters.text, self.group_name)
                ],
                GROUP_WST: [
                    MessageHandler(Filters.text, self.group_wst)
                ],
                GROUP_WCT: [
                    MessageHandler(Filters.text, self.group_wct)
                ],
                GROUP_HST: [
                    MessageHandler(Filters.text, self.group_hst)
                ],
                GROUP_HCT: [
                    MessageHandler(Filters.text, self.group_hct)
                ],
            },
            fallbacks=[CommandHandler('cancel', self.cancel_interaction)],
        )
