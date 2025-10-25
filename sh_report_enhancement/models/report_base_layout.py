# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_display_header = fields.Boolean('Display Header Image ?')
    sh_header_image = fields.Binary('Header Image')
    sh_display_footer = fields.Boolean('Display Footer Image ?')
    sh_footer_image = fields.Binary('Footer Image')


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    sh_display_header = fields.Boolean(
        'Display Header Image ?', related='company_id.sh_display_header', readonly=False)
    sh_header_image = fields.Binary(
        'Header Image', related='company_id.sh_header_image', readonly=False)
    sh_display_footer = fields.Boolean(
        'Display Footer Image ?', related='company_id.sh_display_footer', readonly=False)
    sh_footer_image = fields.Binary(
        'Footer Image', related='company_id.sh_footer_image', readonly=False)
