from odoo import fields, models, api
from datetime import datetime

class HrEmployeeTransferApprove(models.TransientModel):
    _name = 'hr.employee.transfer.approve'
    _description = 'Hr employee transfer'
    _rec_name = 'employee_id'


    assign_task = fields.Boolean(string = 'Assign tasks to another employee?', defaut = 'False')
    name = fields.Many2one('res.users', string = 'Slect another user')
    employee_id = fields.Many2one('hr.employee.transfer', readonly=1)


    def transfer_assigned_to(self):
        if self.name:
            self.employee_id.employee_id.address_id = self.employee_id.transfer_to.partner_id
            serch_id = self.env['mail.activity'].search([('user_id', '=', self.employee_id.employee_id.user_id.id)])
            for mail_act in serch_id:
                mail_act.user_id = self.employee_id.id
