from odoo import models, fields, api,_
from datetime import datetime, date


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = "Payslip"

    @api.multi
    def action_payslip_done(self):
        res =  super(HrPayslip, self).action_payslip_done()
        pf_balance = self.env['pf.employee'].search([('employee_id','=',self.employee_id.id)],limit=1)
        print('===============pf employee========================',pf_balance.id)
        pf_details_ids = []
        if res:
            print('===============pf employee 2========================', pf_balance.id)
            if pf_balance:
                print('===============pf employee 3========================', pf_balance.id)
                for record in pf_balance:
                    print('===============pf employee 4========================', pf_balance.id)
                    if self.line_ids:
                        print('===============pf employee 5========================', pf_balance.id)
                        for i in self.line_ids:
                            if i.salary_rule_id.pf_register == True:
                                print('===============pf employee6========================', pf_balance.id)
                                create_pf_details = self.env['pf.employee.details'].create(
                                    {
                                        'pf_details_id': record.id,
                                        'employee_id': record.employee_id.id,
                                        'type': 'Deposit',
                                        'pf_code': i.code,
                                        'description': i.name,
                                        'date': datetime.now().date(),
                                        'amount': i.total,
                                        'reference': res.number,
                                    }
                                )
                                print('===============pf create_pf_details========================', create_pf_details.id)
                        #         pf_details_ids.append((0, 0, {
                        #             'pf_details_id': record.id,
                        #             'employee_id': record.employee_id.id,
                        #             'type': 'Deposit',
                        #             'pf_code': i.code,
                        #             'description': i.name,
                        #             'date': datetime.now().date(),
                        #             'amount': i.total,
                        #             'reference': res.number,
                        #         }))
                        # record.pf_details_ids = pf_details_ids
        return self