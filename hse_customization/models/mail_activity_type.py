from odoo import api, models


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = list(args or [])
        # Restrict to HSE when the context says so or when used on x_hse model
        res_model = self.env.context.get("default_res_model") or self.env.context.get("res_model")
        if res_model == "x_hse":
            args.append(("res_model", "=", "x_hse"))
        return super().name_search(name, args=args, operator=operator, limit=limit)
