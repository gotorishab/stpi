from odoo import models, fields, api,_
from datetime import datetime, date


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = "Payslip"

    @api.multi
    def action_payslip_done(self):
        res =  super(HrPayslip, self).action_payslip_done()
        pf_balance = self.env['pf.employee'].search([('employee_id','=',self.employee_id.id)],limit=1)
        pf_details_ids = []
        if res:
            if pf_balance:
                for record in pf_balance:
                    if res.line_ids:
                        for i in res.line_ids:
                            if i.salary_rule_id.pf_register == True:
                                pf_details_ids.append((0, 0, {
                                    'pf_details_id': record.id,
                                    'employee_id': record.employee_id.id,
                                    'type': 'Deposit',
                                    'pf_code': i.code,
                                    'description': i.name,
                                    'date': datetime.now().date(),
                                    'amount': i.total,
                                    'reference': res.number,
                                }))
                        record.pf_details_ids = pf_details_ids
            return res