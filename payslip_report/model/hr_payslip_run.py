from odoo import api, fields, models, tools , _

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'  
    
    allow_download = fields.Boolean(string='Allow Download') 
    
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
#                 print("drafttttttttttttttttttttttt",slip.state)
                slip.compute_sheet()
                slip.action_payslip_done()
#                 print("/////////////////////////")
                return self.write({'state': 'close'})
            else:
                self.close_payslip_run()
            
