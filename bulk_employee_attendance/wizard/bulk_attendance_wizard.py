from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class BulkAttendanceWizard(models.TransientModel):
    _name = 'bulk.attendance.wizard'
    _description = 'Bulk Attendance Wizard'


    attendance_type = fields.Selection([
        ('check_in', 'Check In'),
        ('check_out', 'Check Out')
    ], string='Attendance Type', required=True, default='check_in')

    employee_ids = fields.Many2many(
        'hr.employee',
        string='Employees',
        required=True,
        domain=[('id', '!=', False)]
    )

    check_datetime = fields.Datetime(
        string='Date & Time',
        required=True,
        default=fields.Datetime.now
    )

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        help='Project related to this attendance record.'
    )

    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        help='Vehicle used during attendance period (if any).'
    )

    mode = fields.Selection([
        ('manual', 'Manual'),
    ], string='Mode', default='manual', help='Attendance mode')

    @api.constrains('check_datetime')
    def _check_datetime(self):
        """Validate that the datetime is not in the future"""
        for record in self:
            if self.attendance_type == 'check_in':
                if record.check_datetime > fields.Datetime.now():
                    raise ValidationError(_('You cannot create attendance records for future dates.'))

    def action_create_attendance(self):
        """Create attendance records for selected employees"""
        self.ensure_one()

        if not self.employee_ids:
            raise UserError(_('Please select at least one employee.'))

        attendance_obj = self.env['hr.attendance']
        created_attendances = self.env['hr.attendance']
        errors = []
        success_count = 0

        for employee in self.employee_ids:
            try:
                if self.attendance_type == 'check_in':
                    # Check if employee already has an open attendance
                    open_attendance = attendance_obj.search([
                        ('employee_id', '=', employee.id),
                        ('check_out', '=', False)
                    ], limit=1)

                    if open_attendance:
                        errors.append(_('Employee %s already has an open attendance record.') % employee.name)
                        continue

                    # Create check-in
                    attendance = attendance_obj.create({
                        'employee_id': employee.id,
                        'check_in': self.check_datetime,
                        'x_studio_project': self.project_id.id,
                        'x_studio_vehicle': self.vehicle_id.id
                    })
                    created_attendances |= attendance
                    success_count += 1

                else:  # check_out
                    # Find the open attendance record
                    open_attendance = attendance_obj.search([
                        ('employee_id', '=', employee.id),
                        ('check_out', '=', False)
                    ], order='check_in desc', limit=1)

                    if not open_attendance:
                        errors.append(
                            _('Employee %s does not have an open attendance record to check out.') % employee.name)
                        continue

                    # Validate check-out is after check-in
                    if self.check_datetime <= open_attendance.check_in:
                        errors.append(_('Check-out time for %s must be after check-in time (%s).') % (
                            employee.name,
                            open_attendance.check_in.strftime('%Y-%m-%d %H:%M:%S')
                        ))
                        continue

                    # Update with check-out
                    open_attendance.write({
                        'check_out': self.check_datetime,
                    })
                    created_attendances |= open_attendance
                    success_count += 1

            except Exception as e:
                errors.append(_('Error processing employee %s: %s') % (employee.name, str(e)))

        # Prepare result message
        if created_attendances:
            if self.attendance_type == 'check_in':
                message = _('%d employee(s) checked in successfully.') % success_count
            else:
                message = _('%d employee(s) checked out successfully.') % success_count

            if errors:
                message += '\n\n' + _('Warnings:') + '\n' + '\n'.join(errors)

            # Show success notification
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': message,
                    'type': 'success',
                    'sticky': True,  # Make it sticky so user can see it
                    'next': {
                        'type': 'ir.actions.act_window_close',  # Close wizard first
                    }
                }
            }
        else:
            # Only errors occurred
            error_message = _('No attendance records were created.') + '\n\n' + '\n'.join(errors)
            raise UserError(error_message)

    def action_cancel(self):
        """Cancel the wizard"""
        return {'type': 'ir.actions.act_window_close'}