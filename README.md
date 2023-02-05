# CMS

## Commands

1. `python manage.py runserver` - to run the admin panel
2. `python manage.py run_bot` - to run the telegram bot
3. `python manage.py run_huey` - to run the background processes

## API Endpoints

- `POST /api/attendance/log/` - log attendance

- `GET /api/attendance/profile/<user_id>/` - get attendance statistics for a user
- `GET /api/attendance/date/<date:YYYY-MM-DD>/` - get attendance statistics summary for a date
- `GET /api/attendance/date/<date:YYYY-MM-DD>/group/<group_id>/` - get attendance report for a group on a date
- `GET /api/attendance/date/<date:YYYY-MM-DD>/gender/<>/` - get attendance report for a user on a date
