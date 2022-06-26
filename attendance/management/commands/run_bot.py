from django.core.management import BaseCommand

from cms.utils.telegram import ChowkidarBot


class Command(BaseCommand):
    help = 'Runs our telegram bot'

    def handle(self, *args, **options):
        bot = ChowkidarBot()
        bot.start_bot()

