# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductRequestFormPr(models.Model):
    # _name = "vit.product.request"
    _inherit = "vit.product.request"

    description = fields.Text(string="Description")