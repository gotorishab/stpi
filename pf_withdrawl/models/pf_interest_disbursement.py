from odoo import models, fields, api,_


class PfInterestDisbursement(models.Model):
    _name = 'pf.interest.disbursement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'pf.interest.disbursement'

    branch_id = fields.Many2many('res.branch')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    interest_rate = fields.Float('Interest Rate')

