from odoo import models, fields, api,_


class PfInterestDisbursement(models.Model):
    _name = 'pf.interest.disbursement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'pf.interest.disbursement'

    branch_id = fields.Many2many('res.branch')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    interest_rate = fields.Float('Interest Rate')


    @api.constrains('from_date','to_date','branch_id')
    @api.onchange('from_date','to_date','branch_id')
    def onchange_date_branch_gi(self):
        for rec in self:
            company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)], limit=1)
            if company:
                for com in company:
                    if rec.from_date and rec.to_date and rec.branch_id:
                        for line in com.pf_table:
                            if line.from_date >= rec.from_date and line.to_date <= rec.to_date:
                                rec.interest_rate = line.interest_rate


    @api.multi
    def button_submit(self):
        pass