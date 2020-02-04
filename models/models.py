# -*- coding: utf-8 -*-
from odoo import tools
from odoo import models, fields, api, _
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
    _name = "vit.product.request"
    _inherit = ['vit.product.request','mail.thread']

    description = fields.Text(string="Description")
    requesto_id = fields.Many2one(comodel_name='res.users', string='Requester',required=True,default=lambda self: self.env.uid)
    reviewed_by = fields.Many2one(comodel_name='hr.employee', states={'draft':[('readonly',True)],'open':[('readonly',True)],'onprogress':[('readonly',False),('required',True)],'reviewed':[('readonly',True)],'budgetconfirm':[('readonly',True)],'approved':[('readonly',True)],'done':[('readonly',True)],'reject':[('readonly',True)]},string='Reviewed by')
    budgeted_by = fields.Many2one(comodel_name='hr.employee', states={'draft':[('readonly',True)],'open':[('readonly',True)],'onprogress':[('readonly',True)],'reviewed':[('readonly',False),('required',True)],'budgetconfirm':[('readonly',True)],'approved':[('readonly',True)],'done':[('readonly',True)],'reject':[('readonly',True)]},string='Budget Confirmed')
    approved_by = fields.Many2one(comodel_name='hr.employee', states={'draft':[('readonly',True)],'open':[('readonly',True)],'onprogress':[('readonly',True)],'reviewed':[('readonly',True)],'budgetconfirm':[('readonly',False),('required',True)],'approved':[('readonly',True)],'done':[('readonly',True)],'reject':[('readonly',True)]},string='Approved by')
    state = fields.Selection(PR_STATES,'Status',readonly=True,required=True, default='draft',track_visibility='onchange')
    # analytic_account = fields.Many2one(comodel_name='account.analytic.account', string="Analytic Account", related="department_id.analytic_account_id")
    analytic_tag_ids = fields.Many2one(comodel_name='account.analytic.tag', string='Location', domain=[('analytic_dimension_id.name','=','LOCATION')])
    bisnis = fields.Many2one(comodel_name='account.analytic.tag', string='Business', domain=[('analytic_dimension_id.name','=','BUSINESS')])
    category_id = fields.Many2one(comodel_name='product.category', string='Product Category', required=False, readonly=True, states={'draft':[('readonly',False)]},track_visibility='onchange')
    # product_request_aproval_level_ids = fields.One2many(string='Approval Level Line',ondelete="cascade", copy= True,)
    
    @api.model
    def find_notif_users(self,vals):
        requesto_ids = []
        if requesto_ids:
                vals['message_follower_ids'] = [(0,0, {
                    'res_model':'vit.product.request',
                    'requesto_id':self.env['requesto_id']})]
        
    @api.multi
    def send_followers(self, body):
        # to inbox followers and write notes
        # followers = [x.requesto_id.id for x in
        #     self.message_follower_ids]
        self.message_post(body=body,
            type="notification", subtype="mt_comment",
            requesto_ids=self.requesto_id)
        return
    
    def send_to_channel(self, body):
        ch_obj = self.env['mail.channel']
        ch = ch_obj.sudo().search([('name','ilike',
            'via, Mitchell Admin')])    
        body = _("complete")
        ch.message_post( attachment_ids=[], body=body,
            content_subtype='html', message_type='comment',
            requesto_ids=[], subtype='mail.mt_comment')
        return True

    
    @api.multi
    def action_draft(self):
        #set to "draft" state
        body = _("PR set to draft")
        # self.send_followers(body)
        self.update_line_state(PR_STATES[0][0])
        return self.write({'state':PR_STATES[0][0]})

    @api.multi
    def action_confirm(self,body):
        #set to "open" approved state
        # body = _("PR confirmed")
        # self.env['mail.message'].create({'message_type':"notification",
        #         "subtype": self.env.ref("mail.mt_comment").id, # subject type
        #         'body': "Message body",
        #         'subject': "Message subject",
        #         'needaction_partner_ids': [(4, self.user_id.requesto_id.id)],   # partner to whom you send notification
        #         'model': self._name,
        #         'res_id': self.id,
        #         })
        self.send_followers(body)
        self.send_to_channel(body)
        self.update_line_state(PR_STATES[1][0])
        return self.write({'state':PR_STATES[1][0]})

    @api.multi
    def action_confirm_request(self):
        #set to "open" approved state
        body = _("PR confirmed")
        # self.send_to_channel(body)
        self.update_line_state(PR_STATES[2][0])
        return self.write({'state':PR_STATES[2][0]})

    @api.multi
    def action_onprogress(self):
        #set to "onprogress" state
        body = _("PR on progress")
        # self.send_followers(body)
        self.update_line_state(PR_STATES[3][0])
        return self.write({'state':PR_STATES[3][0]})

    @api.multi
    def action_reviewed(self):
        body = _("PR Reviewed")
        # self.send_followers(body)
        # self.send_to_channel(body)
        self.update_line_state(PR_STATES[4][0])
        return self.write({'state':PR_STATES[4][0]})

    @api.multi
    def action_budgetconfirm(self):
        body = _("Budget confirmed")
        # self.send_followers(body)
        # self.send_to_channel(body)
        self.update_line_state(PR_STATES[5][0])
        return self.write({'state':PR_STATES[5][0]})

    @api.multi
    def action_approved(self):
        body = _("PR Approved")
        self.update_line_state(PR_STATES[6][0])
        return self.write({'state':PR_STATES[6][0]})

    @api.multi
    def action_reject(self):
        body = _("PR reject")
        self.update_line_state(PR_STATES[7][0])
        return self.write({'state':PR_STATES[7][0]})