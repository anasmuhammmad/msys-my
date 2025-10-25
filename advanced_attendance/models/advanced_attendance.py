from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class AdvancedAttendance(models.Model):
    _name = 'advanced.attendance'
    _description = 'Advanced Attendance Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )

    employee_ids = fields.Many2many(
        'hr.employee',
        string='Employees',
        required=True,
        help="Select employees for check-in/check-out records"
    )

    date_start = fields.Datetime(
        string='Start Date',
        required=True,
        help="Start date and time for the period"
    )

    date_end = fields.Datetime(
        string='End Date',
        required=True,
        help="End date and time for the period"
    )

    check_in_time = fields.Datetime(
        string='Check In Time',
        required=True,
        help="Check-in time for selected employees"
    )

    check_out_time = fields.Datetime(
        string='Check Out Time',
        required=True,
        help="Check-out time for selected employees"
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    created_attendance_count = fields.Integer(
        string='Created Attendances',
        compute='_compute_created_attendance_count'
    )

    note = fields.Text(string='Internal Notes')

    @api.depends('employee_ids')
    def _compute_created_attendance_count(self):
        for record in self:
            record.created_attendance_count = self.env['hr.attendance'].search_count([
                ('advanced_attendance_id', '=', record.id)
            ])

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start >= record.date_end:
                raise ValidationError(_("End date must be after start date."))

    @api.constrains('check_in_time', 'check_out_time')
    def _check_times(self):
        for record in self:
            if record.check_in_time >= record.check_out_time:
                raise ValidationError(_("Check-out time must be after check-in time."))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('advanced.attendance') or _('New')
        return super().create(vals)

    def action_confirm(self):
        """Confirm the advanced attendance record"""
        for record in self:
            if record.state != 'draft':
                continue

            # Validate employees
            if not record.employee_ids:
                raise ValidationError(_("Please select at least one employee."))

            # Validate times
            if not record.check_in_time or not record.check_out_time:
                raise ValidationError(_("Please set both check-in and check-out times."))

            record.state = 'confirmed'

        return True

    def action_generate_attendances(self):
        """Generate attendance records for selected employees"""
        for record in self:
            if record.state != 'confirmed':
                raise ValidationError(_("Only confirmed records can generate attendances."))

            attendance_obj = self.env['hr.attendance']
            created_count = 0

            for employee in record.employee_ids:
                # Check for existing attendance conflicts
                existing_attendance = attendance_obj.search([
                    ('employee_id', '=', employee.id),
                    ('check_in', '<=', record.check_in_time),
                    ('check_out', '>=', record.check_out_time),
                ])

                if existing_attendance:
                    _logger.warning(f"Attendance conflict for employee {employee.name}. Skipping.")
                    continue

                # Create attendance record
                attendance_vals = {
                    'employee_id': employee.id,
                    'check_in': record.check_in_time,
                    'check_out': record.check_out_time,
                    'advanced_attendance_id': record.id,
                }

                attendance_obj.create(attendance_vals)
                created_count += 1

            if created_count > 0:
                record.state = 'done'
                message = _("Created %d attendance records successfully.") % created_count
                record.message_post(body=message)
            else:
                raise ValidationError(
                    _("No attendance records were created. There might be conflicts with existing attendances."))

        return True

    def action_reset_to_draft(self):
        """Reset record to draft state"""
        for record in self:
            record.state = 'draft'
        return True

    def action_cancel(self):
        """Cancel the advanced attendance record"""
        for record in self:
            # Delete related attendance records
            attendances = self.env['hr.attendance'].search([
                ('advanced_attendance_id', '=', record.id)
            ])
            attendances.unlink()

            record.state = 'cancel'
        return True

    def action_view_created_attendances(self):
        """View created attendance records"""
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('hr_attendance.hr_attendance_action')
        action['domain'] = [('advanced_attendance_id', '=', self.id)]
        action['context'] = {'search_default_employee': 1}
        return action