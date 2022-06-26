from django.core.management import BaseCommand

from attendance.utils.bluetooth import get_bluetooth_address


class Command(BaseCommand):
    help = 'Runs our telegram bot'

    def handle(self, *args, **options):
        arr = get_bluetooth_address()
        for a in arr:
            print(a)

