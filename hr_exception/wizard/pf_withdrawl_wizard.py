
from odoo import api, fields, models

class PFWidthdrawlConfirm(models.TransientModel):
    _name = 'employee.pf.widthdrawl.confirm'
    _inherit = ['exception.rule.confirm']

    related_model_id = fields.Many2one('pf.widthdrawl', 'PF Widthdrawl')

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        if self.ignore:
            self.related_model_id.ignore_exception = True
        return super(PFWidthdrawlConfirm, self).action_confirm()
