# -*- coding: utf-8 -*-
from odoo import http

# class VitProductRequestFormPr(http.Controller):
#     @http.route('/vit_product_request_form_pr/vit_product_request_form_pr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_product_request_form_pr/vit_product_request_form_pr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_product_request_form_pr.listing', {
#             'root': '/vit_product_request_form_pr/vit_product_request_form_pr',
#             'objects': http.request.env['vit_product_request_form_pr.vit_product_request_form_pr'].search([]),
#         })

#     @http.route('/vit_product_request_form_pr/vit_product_request_form_pr/objects/<model("vit_product_request_form_pr.vit_product_request_form_pr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_product_request_form_pr.object', {
#             'object': obj
#         })