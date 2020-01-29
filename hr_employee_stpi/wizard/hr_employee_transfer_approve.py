from odoo import fields, models, api
from datetime import datetime

class HrEmployeeTransferApprove(models.TransientModel):
    _name = 'hr.employee.transfer.approve'
    _description = 'Hr employee transfer'
    _rec_name = 'employee_id'


    assign_task = fields.Boolean(string = 'Assign tasks to another employee?', defaut = 'False')
    name = fields.Many2one('res.users', string = 'Slect another user')
    employee_id = fields.Many2one('hr.employee.transfer', invisible=1)


    def transfer_assigned_to(self):
        if self.name:
            self.employee_id.employee_id.address_id = self.employee_id.to_location
            serch_id = self.env['ir.model'].search([('model', '=','hr.employee')])
            cre = self.env['mail.activity'].create(
                {
                    'res_id':self.employee_id.id,
                    'res_model_id':serch_id.id,
                    'user_id': self.name.id,
                    'date_deadline':datetime.now().date(),
                    'activity_type_id': 4,
                }
            )
