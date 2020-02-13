from odoo import api, fields, models, tools , _

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'   
    
    @api.multi
    def compute_payslips(self):
        for slip in self.slip_ids:
            if slip.state == 'draft':
                slip.compute_sheet()
                
    @api.multi
    def cancel_payslip_run(self):
#         print"We are in new inherited button method"
        for slip in self.slip_ids:
            if slip.state == 'draft':
                slip.action_payslip_cancel()
                return self.write({'state': 'close'})
