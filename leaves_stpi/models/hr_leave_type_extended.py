
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import date
import datetime
from odoo.tools.float_utils import float_round

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'
    _description = 'HR Leave Type Changes For STPI'
    
    @api.one
    @api.depends('creadit_policy_id.no_pf_leaves_credit')
    def _compute_amount(self):
#         round_curr = self.currency_id.round
        amt = 0.0
        for line in self.creadit_policy_id:
            amt += line.no_pf_leaves_credit
#             print("????????????????????????",amt)
            self.amount_total = amt
#             print("///////////////////////",self.amount_total)
        return amt
    
    name = fields.Selection([('Casual Leave','Casual Leave'),
                               ('Half Pay Leave','Half Pay Leave'),
#                                 ('Commuted Leave','Commuted Leave'),
                               ('Earned Leave','Earned Leave'),
                               ('Maternity Leave','Maternity Leave'),
                               ('Special Casual Leave','Special Casual Leave'),
                               ('Extra Ordinary Leave','Extra Ordinary Leave'),
                               ('Paternity Leave','Paternity Leave'),
                               ('Child Care Leave','Child Care Leave')
                        ],string='Name',required=True)
    leave_type = fields.Selection([('Casual Leave','Casual Leave'),
                               ('Half Pay Leave','Half Pay Leave'),
#                                 ('Commuted Leave','Commuted Leave'),
                               ('Earned Leave','Earned Leave'),
                               ('Maternity Leave','Maternity Leave'),
                               ('Special Casual Leave','Special Casual Leave'),
                               ('Extra Ordinary Leave','Extra Ordinary Leave'),
                               ('Paternity Leave','Paternity Leave'),
                               ('Child Care Leave','Child Care Leave')
                                ],string="Leave Type",required=True)
    leave_per_year = fields.Integer(string="Leave Per Year",readonly=True)
    carried_forward = fields.Boolean(string="Carried Forward")
    leave_month = fields.Selection([('January','January'),
                                    ('February','February'),
                                    ('March','March'),
                                    ('April','April'),
                                    ('May','May'),
                                    ('June','June'),
                                    ('July','July'),
                                    ('August','August'),
                                    ('September','September'),
                                    ('October','October'),
                                    ('November','November'),
                                    ('December','December')
                                    ],string="Lapse Month")
    allow_service_leave = fields.Many2many('leave.employee.type',string="Allow Service Leave")
    max_encash_leave = fields.Integer(string="Maximum Encash Leave")
    group_id = fields.Many2one('hr.leave.group',string="Group")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    use_balance_from_id = fields.Many2one('leave.type',string="Use Balance From")
    maximum_allow_leave = fields.Integer(string="Maximum Allow Leave")
    allow_gender = fields.Selection([('male','Male'),
                                     ('female','Female'),
                                     ('both','Both')   
                                    ],string="Allow Gender")
    allow_emp_stage = fields.Many2many('leave.type.employee.stage',string="Allow Employee Stage")
    encash_leave = fields.Boolean(string="Encashed Leave")
    cerificate = fields.Boolean(string="Certificate")
    sandwich_rule = fields.Boolean(string="Sandwich Rule")
    creadit_policy_id = fields.One2many('leave.type.credit.policy','leave_policy','Credit Leave Policy')
    commuted = fields.Boolean(string="Commuted")
    amount_total = fields.Monetary(string='Total',store=True, readonly=True, compute='_compute_amount')
    
   
    @api.model
    def create(self, vals):
        res = super(HrLeaveType, self).create(vals)
        leave_type_rec = self.env['hr.leave.type'].search(
            [('name', '=', res.name), ('id', '!=', res.id),('leave_type','=',res.leave_type)])
        if leave_type_rec:
            raise ValidationError(_('Exists ! Already a Leave Type exists in this name'))
        return res
    
    @api.constrains('amount_total')
    @api.onchange('amount_total')
    def get_leave_per_year(self):
        for leave in self:
            leave.leave_per_year = leave.amount_total

    @api.constrains('leave_type')
    @api.onchange('leave_type')
    def get_name(self):
        for leave in self:
            leave.name = leave.leave_type
            print("leave^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6",leave.name)
            
    @api.multi
    def button_expried_leaves(self):
        for leave in self:
            mydate = datetime.datetime.now()
            month = mydate.strftime("%B")
            for service_leave in leave.allow_service_leave:
                for emp_stages in leave.allow_emp_stage:
                    print("????????????????????????????",month)
                    if leave.leave_month == month:
                        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                        if leave.allow_gender == 'male' or leave.allow_gender =='female':
    #                                 print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
                            employee_ids = self.env['hr.employee'].search([('gender','=',leave.allow_gender),
                                                                           ('employee_type','=',service_leave.tech_name),
                                                                           ('state','=',emp_stages.tech_name),
                                                                           ('active','=',True)
                                                                           ])
                        elif leave.allow_gender == 'both':
                            print("BBBBBBBBBBBBBBBBBBBBBBBBBB",service_leave.tech_name,emp_stages.tech_name)
                            employee_ids = self.env['hr.employee'].search([('employee_type','=',service_leave.tech_name),
                                                                           ('state','=',emp_stages.tech_name),
                                                                           ('active','=',True)
                                                                           ])
                            print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLL",employee_ids)
                            
                        for employee in employee_ids:
    #                                 print("?????????????zzzzzzzzzzzzzzzzzzzzzzzzzzz?????????????",employee_ids,line.no_pf_leaves_credit)
                            total_leave = 0.0
                            hr_leave_report = self.env['hr.leave.report'].search([('employee_id','=',employee.id),
                                                                                  ('holiday_type','=','employee'),
                                                                                  ('holiday_status_id','=',leave.id),
                                                                                  ('state','=','validate')
                                                                                  ])
                            print("?availabeleaveeeeeeeeee",hr_leave_report)
                            for leave_report in hr_leave_report:
                                total_leave += leave_report.number_of_days
                                print("<<<<<<<<<<}}}}}}}}}}}}}}}}}}",total_leave)
                            if hr_leave_report:
                                hr_leave = self.env['hr.leave'].create({'holiday_status_id': leave.id,
                                                                               'holiday_type': 'employee',
                                                                               'employee_id': employee.id,
                                                                               'request_date_from':date.today(),
                                                                               'request_date_to':date.today(),
                                                                               'number_of_days_display':total_leave,
                                                                               'number_of_days':total_leave
                                                                               })
#                                 print("allocationnnnnnnnnnnnn",hr_leave)
                                hr_leave.sudo().action_approve()
                                if hr_leave:
                                    leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                'hr_employee_id':employee.id,
                                                                                                'holiday_status_id':leave.id,
                                                                                                'date':date.today(),
                                                                                                'leave_info':'debit',
                                                                                                'no_of_days':total_leave
                                                                                            })
#                                     print("???????<<<<<<<<<<<<<<<<<<<<<???????????????",leave_bal_id)

    @api.multi
    def button_allocate_leaves(self):
        for leave in self:
            mydate = datetime.datetime.now()
            month = mydate.strftime("%B")
            print("Monttttttttttt",month)
            today = date.today()
            for line in leave.creadit_policy_id:
                for service_leave in leave.allow_service_leave:
                    for emp_stages in leave.allow_emp_stage:
#                         print("????????????????????????????",line.day,line.month)
                        if line.day == today.day and line.month == month:
                            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                            if leave.allow_gender == 'male' or leave.allow_gender =='female':
#                                 print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
                                employee_ids = self.env['hr.employee'].search([('gender','=',leave.allow_gender),
                                                                               ('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
                                                                               ('active','=',True)
                                                                               ])
                            elif leave.allow_gender == 'both':
                                print("BBBBBBBBBBBBBBBBBBBBBBBBBB",service_leave.name,emp_stages.name)
                                employee_ids = self.env['hr.employee'].search([('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
                                                                               ('active','=',True)
                                                                               ])
                                print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLL",employee_ids)
                            for employee in employee_ids:
                                print("?????????????zzzzzzzzzzzzzzzzzzzzzzzzzzz?????????????",employee_ids,line.no_pf_leaves_credit)
                                if employee:
                                    allocate_leave = self.env['hr.leave.allocation'].create({'holiday_status_id': leave.id,
                                                                                   'holiday_type': 'employee',
                                                                                   'employee_id': employee.id,
                                                                                   'number_of_days_display':line.no_pf_leaves_credit,
                                                                                   'number_of_days':line.no_pf_leaves_credit,
                                                                                   'name':'System Leave Allocation',
                                                                                   'notes':'As Per Leave Policy'
                                                                                   })
#                                     print("allocationnnnnnnnnnnnn",allocate_leave)
                                    allocate_leave.sudo().action_approve()
                                    
                                    if allocate_leave:
                                        leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                'hr_employee_id':employee.id,
                                                                                                'holiday_status_id':leave.id,
                                                                                                'date':date.today(),
                                                                                                'leave_info':'credit',
                                                                                                'no_of_days':line.no_pf_leaves_credit
                                                                                            })
                                        print("??????????????????????",leave_bal_id)
                                
                
class LeaveTypeCreditPolicy(models.Model):
    _name = 'leave.type.credit.policy'
    _description = 'Leave Policy'
    
    leave_policy = fields.Many2one('hr.leave.type',string="Leave Type")
    day = fields.Integer(string="Day")
    month = fields.Selection([('January','January'),
                                ('February','February'),
                                ('March','March'),
                                ('April','April'),
                                ('May','May'),
                                ('June','June'),
                                ('July','July'),
                                ('August','August'),
                                ('September','September'),
                                ('October','October'),
                                ('November','November'),
                                ('December','December')
                            ],string="Month")
    no_pf_leaves_credit = fields.Integer(string="No Of Leaves Creadit")
    
    
class LeaveGrroup(models.Model):
    _name = 'hr.leave.group'
    _description = 'Leave Group'
    _rec_name = 'name'
    
    name = fields.Char(string="Name")
    