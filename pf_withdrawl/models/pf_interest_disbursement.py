from odoo import models, fields, api,_
from datetime import datetime, date


class PfInterestDisbursement(models.Model):
    _name = 'pf.interest.disbursement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'pf.interest.disbursement'

    branch_id = fields.Many2many('res.branch', track_visibility='always')
    from_date = fields.Date('From Date', track_visibility='always')
    to_date = fields.Date('To Date', track_visibility='always')
    interest_rate = fields.Float('Interest Rate', track_visibility='always')


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
        # for rec in self:
        #     pf_details_ids = []
        #     pf_emp = self.env['pf.employee'].search([('employee_id.branch_id', 'in', rec.branch_id.ids)])
        #     for line in pf_emp:
        #         pf_details_ids.append((0, 0, {
        #             'pf_details_id': rec.id,
        #             'employee_id': line.employee_id.id,
        #             'type': 'Deposit',
        #             'pf_code': line.code,
        #             'description': line.name,
        #             'date': datetime.now().date(),
        #             'amount': line.total,
        #             'reference': line.slip_id.number,
        #         }))
        #         line.pf_details_ids = a = pf_details_ids