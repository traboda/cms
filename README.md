# CMS

A set of powerful backend APIs to help run the clubs. CMS streamlines various internal processes in running
a student club, such as attendance, member management, and more.

## Commands

1. `python manage.py runserver` - to run the admin panel
2. `python manage.py run_bot` - to run the telegram bot
3. `python manage.py run_huey` - to run the background processes

## API Endpoints

### Attendance

- `POST /api/attendance/log/` - log attendance
- `GET /api/attendance/profile/<user_id>/` - get attendance statistics for a user

#### Live Attendance

- `GET /api/attendance/live/` - get live attendance
- `GET /api/attendance/live/group/<group_id>/` - get live attendance for a group
- `GET /api/attendance/live/gender/<1 | 2>/` - get live attendance for a gender

#### Date-wise Attendance Summary / Report

- `GET /api/attendance/date/<date:YYYY-MM-DD>/` - get attendance statistics summary for a date
- `GET /api/attendance/date/<date:YYYY-MM-DD>/group/<group_id>/` - get attendance report for a group on a date
- `GET /api/attendance/date/<date:YYYY-MM-DD>/gender/<1 | 2>/` - get attendance report for a gender on a date

# License

(c) Traboda CyberLabs Private Limited 2022-2023. All rights reserved.
