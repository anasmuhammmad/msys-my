from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    journal_entry_id = fields.Many2one(
        'account.move',
        string="Internal Transfer Journal Entry",
        readonly=True,
        help="The latest journal entry related to this internal transfer."
    )

    def action_open_journal_entry(self):
        """ Open the last journal entry related to this internal transfer """
        self.ensure_one()
        if not self.journal_entry_id:
            raise UserError(_("No journal entry is linked to this transfer."))
        return {
            'type': 'ir.actions.act_window',
            'name': _("Journal Entry"),
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.journal_entry_id.id,
            'target': 'current',
        }

    def _create_internal_transfer_journal_entry(self):
        """Creates one total debit line and multiple credit lines using product category stock properties"""
        for picking in self:
            if picking.picking_type_id.code != 'internal' or picking.state != 'done':
                continue

            move_lines = picking.move_ids.filtered(lambda m: m.product_id.valuation == 'real_time')
            if not move_lines:
                continue

            journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)
            if not journal:
                raise UserError(_("No general journal found for internal transfers."))

            total_amount = 0.0
            credit_lines = []
            debit_account = None

            for move in move_lines:
                product = move.product_id
                category = product.categ_id

                qty = move.product_uom_qty or sum(move.move_line_ids.mapped('qty_done'))
                cost = product.standard_price
                amount = qty * cost
                total_amount += amount

                credit_account = category.property_stock_account_output_categ_id
                if not credit_account:
                    raise UserError(_("Missing Stock Output Account in product category '%s'" % category.name))

                credit_lines.append((0, 0, {
                    'account_id': credit_account.id,
                    'debit': 0.0,
                    'credit': amount,
                    'name': f"Stock Moved from {picking.location_id.name} ({product.display_name})"
                }))

                # Use the input account of the first product as debit account
                if not debit_account:
                    debit_account = category.property_stock_account_input_categ_id
                    if not debit_account:
                        raise UserError(_("Missing Stock Input Account in product category '%s'" % category.name))

            # Single total debit line
            debit_line = (0, 0, {
                'account_id': debit_account.id,
                'debit': total_amount,
                'credit': 0.0,
                'name': f"Total Stock Received in {picking.location_dest_id.name}"
            })

            journal_entry = self.env['account.move'].create({
                'journal_id': journal.id,
                'date': fields.Date.today(),
                'ref': f"Internal Transfer: {picking.name}",
                'line_ids': [debit_line] + credit_lines
            })

            journal_entry.action_post()
            journal_entry.button_draft()

            picking.journal_entry_id = journal_entry.id

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self._create_internal_transfer_journal_entry()
        return res
