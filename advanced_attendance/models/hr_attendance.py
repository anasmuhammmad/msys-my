from odoo import models, fields, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    advanced_attendance_id = fields.Many2one(
        'advanced.attendance',
        string='Advanced Attendance',
        readonly=True,
        help="Reference to the advanced attendance record that created this attendance"
    )