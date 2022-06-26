from huey import crontab

from huey.contrib.djhuey import db_periodic_task

from attendance.utils.asus import AsusRouter


@db_periodic_task(crontab(minute='*'))
def log_wifi_attendance():
    asus = AsusRouter()
    clients = asus.get_online_clients()

    from attendance.models import WiFiAttendanceDevice, WiFiAttendanceLog
    for client in clients:
        try:
            device = WiFiAttendanceDevice.objects.get(macAddress=client['mac'])
            WiFiAttendanceLog.objects.create(
                member=device.member,
                device=device,
                ipAddress=client['ip'],
            )
        except WiFiAttendanceDevice.DoesNotExist:
            pass

