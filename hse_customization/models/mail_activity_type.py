from odoo import models, fields, api


class HSEModel(models.Model):
    _inherit = 'x_hse'

    # Override the activity_type_id field with domain filter
    activity_type_id = fields.Many2one(
        'mail.activity.type',
        string='Activity Type',
        domain="[('name', '=', 'Grant Approval')]",  # CRITICAL: This filters the dropdown
        tracking=True,
        help="Only HSE-related activity types are shown"
    )


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    @api.onchange('res_model_id', 'res_model')
    def _onchange_res_model_id(self):
        """Filter activity types when res_model is x_hse"""
        res = super()._onchange_res_model_id()
        if self.res_model == 'x_hse':
            # Return domain to filter activity types in the form view
            return {
                'domain': {
                    'activity_type_id': [('name', '=', 'Grant Approval')]
                }
            }
        return res

    # Override the field definition for activities on HSE model
    activity_type_id = fields.Many2one(
        'mail.activity.type',
        string='Activity Type',
        domain=lambda self: self._get_activity_type_domain(),
        required=True,
        index=True
    )

    def _get_activity_type_domain(self):
        """Dynamic domain based on res_model"""
        if self.res_model == 'x_hse' or self._context.get('default_res_model') == 'x_hse':
            return [('name', '=', 'Grant Approval')]
        return []


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    # Add field to mark HSE-related types
    is_hse_type = fields.Boolean(
        string='HSE Activity Type',
        default=False,
        help="Check this box for HSE-related activity types"
    )

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Filter activity types in dropdown based on context"""
        args = list(args or [])

        # Get the model from context
        res_model = self._context.get('default_res_model') or self._context.get('res_model')

        # If we're on HSE model, only show Grant Approval
        if res_model == 'x_hse':
            args.append(('name', '=', 'Grant Approval'))
            # Alternative: use the is_hse_type field
            # args.append(('is_hse_type', '=', True))

        return super(MailActivityType, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """Filter in search/read operations"""
        args = list(args or [])

        # Get the model from context
        res_model = self._context.get('default_res_model') or self._context.get('res_model')

        # If we're on HSE model, only show Grant Approval
        if res_model == 'x_hse':
            args.append(('name', '=', 'Grant Approval'))

        return super(MailActivityType, self)._search(
            args, offset=offset, limit=limit, order=order,
            count=count, access_rights_uid=access_rights_uid
        )