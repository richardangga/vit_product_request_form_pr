# -*- coding: utf-8 -*-
from odoo import tools
from odoo import models, fields, api
import time
import logging
from odoo.tools.translate import _
from collections import defaultdict
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
PR_STATES =[('draft','Draft'),
    ('open','Confirmed'), 
    ('onprogress','On Progress'), 
    ('reviewed','Reviewed'),
    ('budgetconfirm','Budgeted'),
    ('approved','Approved'),
    ('done','Done'),
    ('reject','Rejected')]
PR_LINE_STATES =[('draft','Draft'),
    ('open','Confirmed'), 
    ('onprogress','On Progress'),
    ('reviewed','Reviewed'),
    ('budgetconfirm','Budgeted'),
    ('approved','Approved'),
    ('done','Done'),# Call for Bids = PO created / done
    ('reject','Rejected')]

class ProductRequestFormPr(models.Model):
    # _name = "vit.product.request"
    _inherit = "vit.product.request"

    description = fields.Text(string="Description")
    requesto_id = fields.Many2one(comodel_name='res.users', string='Requester', required=True,default=lambda self: self.env.uid)
    reviewed_by = fields.Many2one(comodel_name='res.users', string='Reviewed by',default=lambda self: self.env.uid)
    budgeted_by = fields.Many2one(comodel_name='res.users', string='Budget Confirmed',default=lambda self: self.env.uid)
    approved_by = fields.Many2one(comodel_name='res.users', string='Approved by',default=lambda self: self.env.uid)
    state = fields.Selection(PR_STATES,'Status',readonly=True,required=True, default='draft',track_visibility='onchange')
    analytic_account = fields.Many2one(comodel_name='account.analytic.account', string="Analytic Account", related="department_id.analytic_account_id")
    category_id = fields.Many2one(comodel_name='product.category', string='Product Category',
        required=False,
        readonly=True,
        states={'draft':[('readonly',False)]},track_visibility='onchange'
        )
    # product_request_aproval_level_ids = fields.One2many(string='Approval Level Line',ondelete="cascade", copy= True,)
    @api.model
    def find_notif_users(self):
        group_obj = self.requesto_id
        group_ids = group_obj.sudo().search([
            # ('category_id', '=', 'Sales'),
            ('name', '=', 'Manager')])
        return group_ids

    @api.multi
    def action_draft(self):
        #set to "draft" state
        body = _("PR set to draft")
        self.send_followers()
        self.update_line_state(PR_STATES[0][0])
        return self.write({'state':PR_STATES[0][0]})

    @api.multi
    def action_confirm(self):
        #set to "open" approved state
        body = _("PR confirmed")
        group_obj = self.requesto_id
        self.send_followers(group_obj)
        self.send_to_channel(group_obj)
        self.update_line_state(PR_STATES[1][0])
        return self.write({'state':PR_STATES[1][0]})

    @api.multi
    def action_onprogress(self):
        #set to "onprogress" state
        body = _("PR on progress")
        self.send_followers(body)
        self.update_line_state(PR_STATES[2][0])
        return self.write({'state':PR_STATES[2][0]})

    @api.multi
    def action_reviewed(self):
        body = _("PR Reviewed")
        self.send_followers(body)
        self.send_to_channel(body)
        self.update_line_state(PR_STATES[3][0])
        return self.write({'state':PR_STATES[3][0]})

    @api.multi
    def action_budgetconfirm(self):
        body = _("Budget confirmed")
        self.send_followers(body)
        self.send_to_channel(body)
        self.update_line_state(PR_STATES[4][0])
        return self.write({'state':PR_STATES[4][0]})

    @api.multi
    def action_approved(self):
        body = _("PR Approved")
        self.send_followers(body)
        self.send_to_channel(body)
        self.update_line_state(PR_STATES[5][0])
        return self.write({'state':PR_STATES[5][0]})

    @api.multi
    def action_done(self):
        #set to "done" state
        body = _("PR done")
        self.send_followers()
        self.update_line_state(PR_STATES[6][0])
        return self.write({'state':PR_STATES[6][0]})

    @api.multi
    def action_reject(self):
        #set to "reject" state
        body = _("PR reject")
        self.send_followers()
        self.update_line_state(PR_STATES[7][0])
        return self.write({'state':PR_STATES[7][0]})
    
    @api.multi
    def send_followers(self, body):
        # to inbox followers and write notes
        followers = [x.partner_id.id for x in
            self.message_follower_ids]
        self.message_post(body=body,
            type="notification", subtype="mt_comment",
            partner_ids=followers,)
        return
    
    def send_to_channel(self, body):
        ch_obj = self.env['mail.channel']
        ch = ch_obj.sudo().search([('name','ilike',
            'via, Mitchell Admin')])
        body = body + " <a href='#id=%s&view_type=form&model=sale.order&menu_id=138'>%s</a>" % (self.id, self.name)
        ch.message_post( attachment_ids=[], body=body,
            content_subtype='html', message_type='comment',
            partner_ids=[], subtype='mail.mt_comment')
        return True