from huey import crontab

from huey.contrib.djhuey import db_periodic_task

from attendance.utils.asus import AsusRouter
from attendance.utils.bluetooth import get_bluetooth_address


@db_periodic_task(crontab(minute='*'))
def log_wifi_attendance():
    asus = AsusRouter()
    clients = asus.get_online_clients()
    from attendance.models import AttendanceLog, AttendanceDevice
    for client in clients:
        try:
            device = AttendanceDevice.objects.get(macAddress=client['mac'])
            AttendanceLog.objects.create(
                member=device.member,
                device=device,
                type='WIFI',
                ipAddress=client['ip'],
            )
        except AttendanceDevice.DoesNotExist:
            pass


@db_periodic_task(crontab(minute='*'))
def log_bluetooth_attendance():
    addresses = get_bluetooth_address()

    from attendance.models import AttendanceLog, AttendanceDevice
    for client in addresses:
        try:
            device = AttendanceDevice.objects.get(bluetoothAddress=client['address'])
            AttendanceLog.objects.create(
                member=device.member,
                device=device,
                type='BLUETOOTH',
            )
        except AttendanceDevice.DoesNotExist:
            pass
