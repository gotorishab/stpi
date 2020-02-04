from odoo import models, fields, api, exceptions
from datetime import  datetime

class  HrEmployeeTransfer(models.Model):
    _name = "hr.employee.transfer"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'HR Employee Transfer'
    _rec_name='employee_id'

    employee_id =  fields.Many2one('hr.employee',string='Employee', store=True)
    job_id = fields.Many2one('hr.job', string="Functional Designation", store=True)
    branch_id = fields.Many2one('res.branch', string="Branch", store=True)
    department_id = fields.Many2one('hr.department', string="Department", store=True)
    date_of_join = fields.Date('Date of Joining',track_visibility='always')
    emp_stages = fields.Selection([
        ('test_period', 'Probation'),
        ('employment', 'Employment'),
        ('notice_period', 'Notice Period'),
        ('relieved', 'Resigned'),
        ('terminate', 'Terminated'),
        ('retired', 'Retired'),
        ('suspended', 'Suspended'),
        ('superannuation', 'Superannuation'),
        ('deceased', 'Deceased'),
        ('absconding', 'Absconding'),
    ], string='Emplyement Status')

    transfer_to = fields.Many2one('res.branch', string='Transfer To')
    order_number = fields.Char(string='Order Number')
    order_date =  fields.Date(string='Order Date')
    file_number=  fields.Char(string='File Number')
    date   =  fields.Date(string='Date', default=datetime.now().date())
    transfer_attach = fields.Binary('Document')
    emp_activity = fields.Many2many('mail.activity', string = 'Activity')

    state = fields.Selection([
                                ('draft', 'Draft'),
                                ('approval', 'Approval'),
                                ('approved', 'Approved'),
                                ('rejected','Rejected')

                            ], default='draft')


    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_emo_get_basic(self):
        for record in self:
            record.job_id = record.employee_id.job_id
            record.branch_id = record.employee_id.branch_id
            record.department_id = record.employee_id.department_id
            record.date_of_join = record.employee_id.date_of_join
            record.emp_stages = record.employee_id.state
            serch_id = self.env['mail.activity'].search([('user_id', '=', self.employee_id.user_id.id)])
            record.emp_activity = serch_id.ids



    @api.multi
    def button_draft(self):
        for rec in self:
            rec.write({'state': 'approval'})

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.employee_id.branch_id = rec.transfer_to.id
            rec.employee_id.address_id = rec.transfer_to.partner_id.id
            rec.write({'state': 'approved'})

    @api.multi
    def button_rejected(self):
        for rec in self:
            rec.write({'state': 'rejected'})


    def button_assign_to(self):
        if self:
            return {
                'name': 'Employee Transfer',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hr.employee.transfer.approve',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'view_id': self.env.ref('hr_employee_transfer.hr_employee_transfer_approve_form_view').id,
                'context': {
                    'default_employee_transfer_id': self.id,
                    'default_branch_id': self.branch_id.id,
                }
            }



class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    transfers_count = fields.Integer('Transfers count', compute='_compute_transfer_count')


    def _compute_transfer_count(self):
        for line in self:
            comp_model = self.env['hr.employee.transfer'].search([('employee_id', '=', self.id),('state', '=', 'approved')])
            line.transfers_count = len(comp_model)


    def set_employee_transfer(self):
        tree_view_id = self.env.ref('hr_employee_transfer.employeetransfer_show_tree_view')
        return {
            'name': 'Employee Transfer',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'hr.employee.transfer',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'views': [(tree_view_id.id, 'tree')],
            'view_id': tree_view_id.id,
            'domain': [('employee_id', '=', self.id),('state', '=', 'approved')]
        }
