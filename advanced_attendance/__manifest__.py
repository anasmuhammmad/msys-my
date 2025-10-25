{
    'name': 'Advanced Attendance Scheduling',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Schedule future attendance records for employees',
    'description': """
Advanced Attendance Scheduling
=============================
This module allows HR managers to schedule future attendance records for employees.

Features:
---------
✓ Schedule attendance for single future dates
✓ Create attendance for date ranges (multiple days)
✓ Set up recurring attendance patterns (daily, weekly, monthly)
✓ Exclude weekends automatically
✓ Bulk scheduling for multiple employees
✓ Time configuration for check-in/check-out
✓ Preview and summary before creation

Use Cases:
----------
• Project-based attendance scheduling
• Employee training programs
• Shift planning for upcoming periods
• Vacation and leave coverage
• Regular recurring work schedules
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/advanced_attendance_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}