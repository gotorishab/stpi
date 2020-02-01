from odoo import api, models, fields


class ExceptionRule(models.Model):
    _inherit = 'exception.rule'

    rule_group = fields.Selection(
        selection_add=[('tour_request', 'Tour Request')],
    )
    model = fields.Selection(
        selection_add=[
            ('tour.request', 'Tour Request'),

        ])

class TourRequestException(models.Model):
    _inherit = ['tour.request', 'base.exception']
    _name = 'tour.request'
    _order = 'main_exception_id'

    rule_group = fields.Selection(
        selection_add=[('tour_request', 'Tour Request')],
        default='tour_request',
    )

    @api.model
    def test_all_draft_orders(self):
        order_set = self.search([('state', '=', 'waiting_for_approval')])
        order_set.test_exceptions()
        return True


    @api.constrains('ignore_exception', 'employee_journey', 'state')
    def tour_request_check_exception(self):
        if self.state == 'approved':
            self._check_exception()

    @api.onchange('employee_journey')
    def onchange_ignore_exception(self):
        if self.state == 'approved':
            self.ignore_exception = False

    @api.multi
    def button_approved(self):
        if self.detect_exceptions():

            return self._popup_exceptions()
        else:
            return super(TourRequestException, self).button_approved()
    #
    def _tour_request_get_lines(self):
        self.ensure_one()
        return self.employee_journey

    @api.model
    def _get_popup_action(self):
        # print("----------------------------_get_popup_action")
        action = self.env.ref('hr_exception.action_tour_request_confirm')
        return action


class Approvalslist(models.Model):
    _inherit = "approvals.list"

    @api.multi
    def approve(self):
        res = super(Approvalslist, self).approve()
        if res:
            # print("----------------------self.model_id.model", self.model_id.model)
            if self.model_id.model == 'tour.request':
                self.resource_ref.button_approved()
        return res

    @api.multi
    def reject(self):
        res=super(Approvalslist,self).reject()
        if res:
            if self.model_id.model == 'tour.request':
                self.resource_ref.button_reject()
        return res
