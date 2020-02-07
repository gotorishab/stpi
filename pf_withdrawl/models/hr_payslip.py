from odoo import models, fields, api,_

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = "Payslip"
    
    
    @api.multi
    def action_payslip_done(self):
        res =  super(HrPayslip, self).action_payslip_done()
        pf_balance = self.env['pf.employee'].search([('employee_id','=',self.employee_id.id)])
#         print("////////////////////////",pf_balance)
        if pf_balance:
            pf_balance.get_pf_details()
        
        return res