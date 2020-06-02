# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError


class PullInto(models.TransientModel):
    _name = "pull.into.custom"
    _description = "HR Employee Cheque Action"


    @api.multi
    def pull_intos_action_button(self):
        pass
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', []) or []
    #     for employee in self.env['cheque.requests'].browse(active_ids):
    #         if employee.state == 'to_approve':
    #             employee.sudo().button_approved()
    #
    #
    # @api.multi
    # def pull_intos_action_reject_button(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', []) or []
    #     for employee in self.env['cheque.requests'].browse(active_ids):
    #         if employee.state == 'to_approve':
    #             employee.sudo().button_reject()