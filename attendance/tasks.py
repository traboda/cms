from huey import crontab

from huey.contrib.djhuey import db_periodic_task

from attendance.utils.asus import AsusRouter


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
