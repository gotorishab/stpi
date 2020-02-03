from odoo import models, fields, api, exceptions
from datetime import  datetime

class  HrEmployeeTransfer(models.Model):
    _name = "hr.employee.transfer"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hr Employee Transfer'
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
    emp_activity = fields.Many2many('mail.activity', string = 'Activity', domain="[('user_id', '=', self.employee_id.user_id)]")

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
            record.branch_id = record.employee_id.job_id.branch_id
            record.department_id = record.employee_id.department_id
            record.date_of_join = record.employee_id.date_of_join
            record.emp_stages = record.employee_id.state

    @api.multi
    def button_draft(self):
        for rec in self:
            rec.write({'state': 'approval'})

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    @api.multi
    def button_rejected(self):
        for rec in self:
            rec.write({'state': 'rejected'})



    @api.onchange('employee_id')
    def location_change(self):
        if self.employee_id:
            self.from_location = self.employee_id.address_id

