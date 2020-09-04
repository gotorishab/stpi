# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class AccountInvoiceConfirm(models.TransientModel):
    _name = "reimbursement.approve.reject"
    _description = "Reimbursementt"


    @api.multi
    def reimbursement_ar_action_button(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for employee in self.env['reimbursement'].browse(active_ids):
            if employee.state == 'waiting_for_approval':
                employee.sudo().button_approved()


    @api.multi
    def reimbursement_ar_action_reject_button(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for employee in self.env['reimbursement'].browse(active_ids):
            if employee.state == 'waiting_for_approval':
                employee.sudo().button_reject()