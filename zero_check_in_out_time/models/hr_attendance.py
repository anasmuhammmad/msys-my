from odoo import models, fields
from datetime import datetime

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    check_in = fields.Datetime(
        default=lambda self: datetime.now().replace(minute=0, second=0, microsecond=0),
        string='Check In'
    )

    check_out = fields.Datetime(
        default=lambda self: datetime.now().replace(minute=0, second=0, microsecond=0),
        string='Check Out'
    )
