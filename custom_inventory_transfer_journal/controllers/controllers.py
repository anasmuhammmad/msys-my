# -*- coding: utf-8 -*-
# from odoo import http


# class Utom(http.Controller):
#     @http.route('/utom/utom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/utom/utom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('utom.listing', {
#             'root': '/utom/utom',
#             'objects': http.request.env['utom.utom'].search([]),
#         })

#     @http.route('/utom/utom/objects/<model("utom.utom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('utom.object', {
#             'object': obj
#         })

