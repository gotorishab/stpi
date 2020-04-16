from odoo import api, fields, models,_


class SendTdsReminder(models.TransientModel):
    _name = 'create.appraisal'
    _description = 'Send Reminder'

    employee_ids = fields.Many2many('hr.employee', string='Employees')
    abap_period = fields.Many2one('date.range', string='APAR Period')

    def create_appraisal_action_button(self):
        for rec in self:
            for employee in rec.employee_ids:
                emp_contract = self.env['hr.contract'].search(
                    [('employee_id', '=', employee.id), ('state', '=', 'open')], limit=1)
                self.env['appraisal.main'].create({
                    'state': 'draft',
                    'employee_id': employee.id,
                    'abap_period': rec.abap_period.id,
                    'branch_id': employee.branch_id.id,
                    'category_id': employee.category.id,
                    'dob': employee.birthday,
                    'job_id': employee.job_id.id,
                    'struct_id': emp_contract.struct_id.id,
                    'pay_level_id': emp_contract.pay_level_id.id,
                    'pay_level': emp_contract.pay_level.id,
                    'template_id': emp_contract.pay_level_id.template_id.id,
                })