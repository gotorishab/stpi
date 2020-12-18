from odoo import api, models, fields,_
from odoo.exceptions import UserError, ValidationError


class ExceptionRule(models.Model):
    _inherit = 'exception.rule'

    rule_group = fields.Selection(
        selection_add=[('health_manage_fireincident', 'Health Manage fireincident'),
                       ],
    )
    model = fields.Selection(
        selection_add=[
            ('health.manage.fireincident', 'Health Manage fireincident'),
        ])


class HealthManagefireincident(models.Model):
    _inherit = ['health.manage.fireincident', 'base.exception']
    _name = 'health.manage.fireincident'
    _order = 'main_exception_id asc,name desc'

    rule_group = fields.Selection(
        selection_add=[('health_manage_fireincident', 'Health Manage fireincident')],
        default='health_manage_fireincident',
    )

    @api.model
    def test_all_draft_orders(self):
        order_set = self.search([('state', '=', 'confirm')])
        order_set.test_exceptions()
        return True

    @api.constrains('ignore_exception','state')
    def sale_check_exception(self):
        if self.state == 'validate':
            self._check_exception()

    #@api.multi
    def action_draft(self):
        res = super(HealthManagefireincident, self).action_draft()
        orders = self.filtered(lambda s: s.ignore_exception)
        orders.write({
            'ignore_exception': False,
        })
        return res

    #@api.multi
    def button_submit(self):
        if self.detect_exceptions():
            return self._popup_exceptions()
        else:
            return super(HealthManagefireincident, self).button_submit()

    @api.model
    def _get_popup_action(self):
        action = self.env.ref('hr_exception.action_health_manage_fireincident_confirm')
        return action

    #@api.multi
    def button_cancel(self):
        exception = self.env['approvals.list'].search([('resource_ref', '=', 'health.manage.fireincident' + ',' + str(self.id)),
                                                       ('state', '=', 'pending_approval')])
        # print("------------------exception",exception)
        if exception:
            raise UserError(_('Do not allow Pending Approval fireincident for Refuse.'))
        return super(HealthManagefireincident, self).button_cancel()

    #@api.multi
    def action_draft(self):
        exception = self.env['approvals.list'].search([('resource_ref', '=', 'health.manage.fireincident' + ',' + str(self.id)),
                                                       ('state', '=', 'pending_approval')])
        # print("------------------exception",exception)
        if exception:
            raise UserError(_('Do not allow Pending Approval fireincident for Reset.'))
        return super(HealthManagefireincident, self).action_draft()


class Approvalslist(models.Model):
    _inherit = "approvals.list"

    #@api.multi
    def approve(self):
        res = super(Approvalslist, self).approve()
        if res:
            # print("----------------------self.model_id.model", self.model_id.model)
            if self.model_id.model == 'health.manage.fireincident':
                self.resource_ref.button_submit()
        return res

    #@api.multi
    def reject(self):
        res = super(Approvalslist, self).reject()
        if res:
            if self.model_id.model == 'health.manage.fireincident':
                self.resource_ref.button_cancel()
        return res

