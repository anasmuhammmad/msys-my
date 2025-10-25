from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    minimum_hours = fields.Float(string="Default Minimum Hours")
