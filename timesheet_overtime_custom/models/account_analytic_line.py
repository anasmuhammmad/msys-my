from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    minimum_hours = fields.Float(string="Minimum Hours")
    overtime_hours = fields.Float(string="Overtime Hours", compute="_compute_overtime_hours", store=True)

    @api.depends('unit_amount', 'minimum_hours')
    def _compute_overtime_hours(self):
        for line in self:
            line.overtime_hours = max(0.0, (line.unit_amount or 0.0) - (line.minimum_hours or 0.0))

    @api.onchange('employee_id')
    def _onchange_employee_minimum_hours(self):
        if self.employee_id and not self.minimum_hours:
            self.minimum_hours = self.employee_id.minimum_hours or 0.0
