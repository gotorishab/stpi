
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import date
import datetime
from odoo.tools.float_utils import float_round
import calendar

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
    gende = fields.Selection([('male','Male'),
                                     ('female','Female'),
                                     ('transgender','Transgender')   
                                    ],string="Allow Gender")
    allow_emp_stage = fields.Many2many('leave.type.employee.stage',string="Allow Employee Stage")
    encash_leave = fields.Boolean(string="Encashed Leave")
    cerificate = fields.Boolean(string="Certificate")
    sandwich_rule = fields.Boolean(string="Sandwich Rule")
    creadit_policy_id = fields.One2many('leave.type.credit.policy','leave_policy','Credit Leave Policy')
    commuted = fields.Boolean(string="Commuted")
    amount_total = fields.Monetary(string='Total',store=True, readonly=True, compute='_compute_amount')
    
    allowed_prefix_leave = fields.Many2many('leave.type',string="Allowed Prefix Leave")
    mid_year_factor = fields.Float(string="Mid Year Factor",compute="compute_mid_year_factor")
    
    @api.model
    def create(self, vals):
        res = super(HrLeaveType, self).create(vals)
        leave_type_rec = self.env['hr.leave.type'].search(
            [('name', '=', res.name), ('id', '!=', res.id),('leave_type','=',res.leave_type)])
        if leave_type_rec:
            raise ValidationError(_('Exists ! Already a Leave Type exists in this name'))
        return res
    
    @api.depends('leave_per_year')
    def compute_mid_year_factor(self):
        for leave in self:
            leave.mid_year_factor = leave.leave_per_year / 12
    
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
#             print("leave^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6",leave.name)

    

    def cron_expire_leave(self):
        confg = self.env['hr.leave.type'].search([])
        today = date.today()
        year, month = today.year, today.month
        current_month_date = calendar.monthrange(year, month)[1]
#         print("0000000000000000000000000",current_month_date)
        for leave in confg:
            mydate = datetime.datetime.now()
            month = mydate.strftime("%B")
            for service_leave in leave.allow_service_leave:
                for emp_stages in leave.allow_emp_stage:
#                     print("22222222222222222222222222222",month,leave.leave_month)
#                     print("333333333333333333333",today.day,current_month_date)
                    if today.day == current_month_date:
                        if leave.leave_month == month:
                            if leave.gende == 'male' or leave.gende =='female':
        #                                 print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
                                employee_ids = self.env['hr.employee'].search([('gende','=',leave.gende),
                                                                               ('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
                                                                               ('active','=',True)
                                                                               ])
                            elif leave.gende == 'transgender':
    #                             print("BBBBBBBBBBBBBBBBBBBBBBBBBB",service_leave.tech_name,emp_stages.tech_name)
                                employee_ids = self.env['hr.employee'].search([('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
                                                                               ('active','=',True)
                                                                               ])
                                
                            for employee in employee_ids:
    #                                 print("@@@@@@@@@@@@@@@@@@@@@@@@",employee)
                                if employee and not employee.leave_balance_id:
                                    total_leave = 0.0
                                    hr_leave_report = self.env['hr.leave.report'].search([('employee_id','=',employee.id),
                                                                                          ('holiday_type','=','employee'),
                                                                                          ('holiday_status_id','=',leave.id),
                                                                                          ('state','=','validate')
                                                                                          ])
    #                                 print("?availabeleaveeeeeeeeee",hr_leave_report)
                                    for leave_report in hr_leave_report:
                                        total_leave += leave_report.number_of_days
    #                                     print("<<<<<<<<<<}}}}}}}}}}}}}}}}}}",total_leave)
                                    if hr_leave_report:
    #                                     print("1111111111111111111111111111111111",leave.id,employee.ids,date.today(),total_leave)
                                        hr_leave = self.env['hr.leave'].create({'holiday_status_id': leave.id,
                                                                                       'holiday_type': 'employee',
                                                                                       'employee_id': employee.id,
                                                                                       'request_date_from':date.today(),
                                                                                       'request_date_to':date.today(),
                                                                                       'number_of_days_display':total_leave,
                                                                                       'number_of_days':total_leave
                                                                                       })
    #                                     print("allocationnnnnnnnnnn2222222222222222222222nn",hr_leave)
                                        hr_leave.sudo().action_approve()
                                        if hr_leave:
                                            leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                        'hr_employee_id':employee.id,
                                                                                                        'holiday_status_id':leave.id,
                                                                                                        'date':date.today(),
                                                                                                        'leave_info':'debit',
                                                                                                        'no_of_days':total_leave
                                                                                                    })
                                elif employee and employee.leave_balance_id:
                                        for credit_policy in leave.creadit_policy_id:
                                            SQL = """
                                                       
                                                select he.id from 
                                                hr_employee as he
                                                left outer join hr_employee_leave_info as heli on heli.hr_employee_id = he.id
                                                left outer join hr_leave_type as hlt on hlt.id = heli.holiday_status_id
                                                where 
                                                he.id in (%s)
                                                and hlt.leave_type in (%s)
                                                and heli.leave_info = 'debit'
                                                and EXTRACT(DAY FROM heli.date) = '%s'
                                                    """
                                            self.env.cr.execute(SQL, (
                                                employee.id,
                                                leave.leave_type,
                                                credit_policy.day
                                            ))
                                            res = self.env.cr.fetchall()
    #                                         print("??????????????RESSSSSSSSSSSSSSSSSSSSS",res,today.day,today.strftime("%B"),credit_policy.day,credit_policy.month)
                                            if not res:
        #                                     print("???????<<<<<<<<<<<<<<<<<<<<<???????????????",leave_bal_id)
                                                if today.day == credit_policy.day and today.strftime("%B") == credit_policy.month:
                                                    total_leave = 0.0
                                                    hr_leave_report = self.env['hr.leave.report'].search([('employee_id','=',employee.id),
                                                                                                          ('holiday_type','=','employee'),
                                                                                                          ('holiday_status_id','=',leave.id),
                                                                                                          ('state','=','validate')
                                                                                                          ])
    #                                                 print("?availabeleaveeeeeeeeee",hr_leave_report)
                                                    for leave_report in hr_leave_report:
                                                        total_leave += leave_report.number_of_days
    #                                                     print("<<<<<<<<<<}}}}}}}}}}}}}}}}}}",total_leave)
                                                    if hr_leave_report:
    #                                                     print("1111111111111111111111111111111111",leave.id,employee.ids,date.today(),total_leave)
                                                        hr_leave = self.env['hr.leave'].create({'holiday_status_id': leave.id,
                                                                                                       'holiday_type': 'employee',
                                                                                                       'employee_id': employee.id,
                                                                                                       'request_date_from':date.today(),
                                                                                                       'request_date_to':date.today(),
                                                                                                       'number_of_days_display':total_leave,
                                                                                                       'number_of_days':total_leave
                                                                                                       })
    #                                                     print("allocationnnnnnnnnnn2222222222222222222222nn",hr_leave)
                                                        hr_leave.sudo().action_approve()
                                                        print("4444444444444444")
                                                        if hr_leave:
                                                            leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                                        'hr_employee_id':employee.id,
                                                                                                                        'holiday_status_id':leave.id,
                                                                                                                        'date':date.today(),
                                                                                                                        'leave_info':'debit',
                                                                                                                        'no_of_days':total_leave
                                                                                                                    })
                                                    
            
    @api.multi
    def button_expried_leaves(self):
        today = date.today()
        for leave in self:
            mydate = datetime.datetime.now()
            month = mydate.strftime("%B")
            for service_leave in leave.allow_service_leave:
                for emp_stages in leave.allow_emp_stage:
                    if leave.leave_month == month:
                        if leave.gende == 'male' or leave.gende =='female':
    #                                 print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
                            employee_ids = self.env['hr.employee'].search([('gende','=',leave.gende),
                                                                           ('employee_type','=',service_leave.tech_name),
                                                                           ('state','=',emp_stages.tech_name),
                                                                           ('active','=',True)
                                                                           ])
                        elif leave.gende == 'transgender':
#                             print("BBBBBBBBBBBBBBBBBBBBBBBBBB",service_leave.tech_name,emp_stages.tech_name)
                            employee_ids = self.env['hr.employee'].search([('employee_type','=',service_leave.tech_name),
                                                                           ('state','=',emp_stages.tech_name),
                                                                           ('active','=',True)
                                                                           ])
                            
                        for employee in employee_ids:
#                                 print("@@@@@@@@@@@@@@@@@@@@@@@@",employee)
                            if employee and not employee.leave_balance_id:
                                total_leave = 0.0
                                hr_leave_report = self.env['hr.leave.report'].search([('employee_id','=',employee.id),
                                                                                      ('holiday_type','=','employee'),
                                                                                      ('holiday_status_id','=',leave.id),
                                                                                      ('state','=','validate')
                                                                                      ])
#                                 print("?availabeleaveeeeeeeeee",hr_leave_report)
                                for leave_report in hr_leave_report:
                                    total_leave += leave_report.number_of_days
#                                     print("<<<<<<<<<<}}}}}}}}}}}}}}}}}}",total_leave)
                                if hr_leave_report:
#                                     print("1111111111111111111111111111111111",leave.id,employee.ids,date.today(),total_leave)
                                    hr_leave = self.env['hr.leave'].create({'holiday_status_id': leave.id,
                                                                                   'holiday_type': 'employee',
                                                                                   'employee_id': employee.id,
                                                                                   'request_date_from':date.today(),
                                                                                   'request_date_to':date.today(),
                                                                                   'number_of_days_display':total_leave,
                                                                                   'number_of_days':total_leave
                                                                                   })
#                                     print("allocationnnnnnnnnnn2222222222222222222222nn",hr_leave)
                                    hr_leave.sudo().action_approve()
                                    if hr_leave:
                                        leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                    'hr_employee_id':employee.id,
                                                                                                    'holiday_status_id':leave.id,
                                                                                                    'date':date.today(),
                                                                                                    'leave_info':'debit',
                                                                                                    'no_of_days':total_leave
                                                                                                })
                            elif employee and employee.leave_balance_id:
                                    for credit_policy in leave.creadit_policy_id:
                                        SQL = """
                                                   
                                            select he.id from 
                                            hr_employee as he
                                            left outer join hr_employee_leave_info as heli on heli.hr_employee_id = he.id
                                            left outer join hr_leave_type as hlt on hlt.id = heli.holiday_status_id
                                            where 
                                            he.id in (%s)
                                            and hlt.leave_type in (%s)
                                            and heli.leave_info = 'debit'
                                            and EXTRACT(DAY FROM heli.date) = '%s'
                                                """
                                        self.env.cr.execute(SQL, (
                                            employee.id,
                                            leave.leave_type,
                                            credit_policy.day
                                        ))
                                        res = self.env.cr.fetchall()
#                                         print("??????????????RESSSSSSSSSSSSSSSSSSSSS",res,today.day,today.strftime("%B"),credit_policy.day,credit_policy.month)
                                        if not res:
    #                                     print("???????<<<<<<<<<<<<<<<<<<<<<???????????????",leave_bal_id)
                                            if today.day == credit_policy.day and today.strftime("%B") == credit_policy.month:
                                                total_leave = 0.0
                                                hr_leave_report = self.env['hr.leave.report'].search([('employee_id','=',employee.id),
                                                                                                      ('holiday_type','=','employee'),
                                                                                                      ('holiday_status_id','=',leave.id),
                                                                                                      ('state','=','validate')
                                                                                                      ])
#                                                 print("?availabeleaveeeeeeeeee",hr_leave_report)
                                                for leave_report in hr_leave_report:
                                                    total_leave += leave_report.number_of_days
#                                                     print("<<<<<<<<<<}}}}}}}}}}}}}}}}}}",total_leave)
                                                if hr_leave_report:
#                                                     print("1111111111111111111111111111111111",leave.id,employee.ids,date.today(),total_leave)
                                                    hr_leave = self.env['hr.leave'].create({'holiday_status_id': leave.id,
                                                                                                   'holiday_type': 'employee',
                                                                                                   'employee_id': employee.id,
                                                                                                   'request_date_from':date.today(),
                                                                                                   'request_date_to':date.today(),
                                                                                                   'number_of_days_display':total_leave,
                                                                                                   'number_of_days':total_leave
                                                                                                   })
                                                    hr_leave.sudo().action_approve()
                                                    if hr_leave:
                                                        leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                                    'hr_employee_id':employee.id,
                                                                                                                    'holiday_status_id':leave.id,
                                                                                                                    'date':date.today(),
                                                                                                                    'leave_info':'debit',
                                                                                                                    'no_of_days':total_leave
                                                                                                                })
    @api.multi                                                
    def button_mid_year_leave_allocate(self):
        for leave in self:
            mydate = datetime.datetime.now()
            month = mydate.strftime("%B")
            today = date.today()
            for line in leave.creadit_policy_id:
                for service_leave in leave.allow_service_leave:
                    for emp_stages in leave.allow_emp_stage:
                        if line.day == today.day and line.month == month:
                            if leave.gende == 'male' or leave.gende =='female':
                                employee_ids = self.env['hr.employee'].search([('gende','=',leave.gende),
                                                                               ('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
                                                                               ('active','=',True),
                                                                               ])
                            elif leave.gende == 'transgender':
                                employee_ids = self.env['hr.employee'].search([('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
                                                                               ('active','=',True)
                                                                               ('mid_year_factor','=',True)
                                                                               ])
                                print("employeeeeeeeeeee",employee_ids)

    @api.multi
    def button_allocate_leaves(self):
        for leave in self:
            mydate = datetime.datetime.now()
            month = mydate.strftime("%B")
            today = date.today()
            for line in leave.creadit_policy_id:
                for service_leave in leave.allow_service_leave:
                    for emp_stages in leave.allow_emp_stage:
                        if line.day == today.day and line.month == month:
#                             print("333333333333333333333",leave.gende,service_leave.tech_name,emp_stages.tech_name)
                            if leave.gende == 'male' or leave.gende =='female':
                                employee_ids = self.env['hr.employee'].search([('gende','=',leave.gende),
                                                                               ('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
#                                                                                ('active','=',True),
                                                                               ])
#                                 print("444444447----------------",employee_ids)
                            elif leave.gende == 'transgender':
                                employee_ids = self.env['hr.employee'].search([('employee_type','=',service_leave.tech_name),
                                                                               ('state','=',emp_stages.tech_name),
                                                                               ('active','=',True)
                                                                               ])
#                                 print("44444444444444444444444444444444",employee_ids)
                            for employee in employee_ids:
#                                 print("@@@@@@@@@@@@@@@@@@@@@@@@",employee)
                                if employee and not employee.leave_balance_id:
                                    allocate_leave = self.env['hr.leave.allocation'].create({'holiday_status_id': leave.id,
                                                                                   'holiday_type': 'employee',
                                                                                   'employee_id': employee.id,
                                                                                   'number_of_days_display':line.no_pf_leaves_credit,
                                                                                   'number_of_days':line.no_pf_leaves_credit,
                                                                                   'name':'System Leave Allocation',
                                                                                   'notes':'As Per Leave Policy'
                                                                                   })
                                    print("allocationnnnnnnnnnnnn",allocate_leave)
                                    allocate_leave.sudo().action_approve()
                                    
                                    if allocate_leave:
                                        leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                'hr_employee_id':employee.id,
                                                                                                'holiday_status_id':leave.id,
                                                                                                'date':date.today(),
                                                                                                'leave_info':'credit',
                                                                                                'no_of_days':line.no_pf_leaves_credit
                                                                                            })
                                elif employee and employee.leave_balance_id:
                                    for credit_policy in leave.creadit_policy_id:
                                        SQL = """
                                                   
                                            select he.id from 
                                            hr_employee as he
                                            left outer join hr_employee_leave_info as heli on heli.hr_employee_id = he.id
                                            left outer join hr_leave_type as hlt on hlt.id = heli.holiday_status_id
                                            where 
                                            he.id in (%s)
                                            and hlt.leave_type in (%s)
                                            and heli.leave_info = 'credit'
                                            and EXTRACT(DAY FROM heli.date) = '%s'
                                                """
                                        self.env.cr.execute(SQL, (
                                            employee.id,
                                            leave.leave_type,
                                            credit_policy.day
                                        ))
                                        res = self.env.cr.fetchall()
                                        print("??????????????RESSSSSSSSSSSSSSSSSSSSS",res,today.day,today.strftime("%B"),credit_policy.day,credit_policy.month)
                                        if not res:
                                            if today.day == credit_policy.day and today.strftime("%B") == credit_policy.month:
                                                print("#############################################")
                                                allocate_leave = self.env['hr.leave.allocation'].create({'holiday_status_id': leave.id,
                                                                                               'holiday_type': 'employee',
                                                                                               'employee_id': employee.id,
                                                                                               'number_of_days_display':line.no_pf_leaves_credit,
                                                                                               'number_of_days':line.no_pf_leaves_credit,
                                                                                               'name':'System Leave Allocation',
                                                                                               'notes':'As Per Leave Policy'
                                                                                               })
                                                print("allocationnnnnnnnnnnnn",allocate_leave)
                                                allocate_leave.sudo().action_approve()
                                                
                                                if allocate_leave:
                                                    leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                            'hr_employee_id':employee.id,
                                                                                                            'holiday_status_id':leave.id,
                                                                                                            'date':date.today(),
                                                                                                            'leave_info':'credit',
                                                                                                            'no_of_days':line.no_pf_leaves_credit
                                                                                                        })
                                                    
                                                    
    def cron_allocate_leave(self):
        
        confg = self.env['hr.leave.type'].search([])
        for leave in confg:
            mydate = datetime.datetime.now()
            month = mydate.strftime("%B")
            today = date.today()
            year, month = today.year, today.month
            current_month_date = calendar.monthrange(year, month)[1]
#             print("0000000000000000000000000",current_month_date)
            for line in leave.creadit_policy_id:
                for service_leave in leave.allow_service_leave:
                    for emp_stages in leave.allow_emp_stage:
#                         print("333333333333333333333",today.day,current_month_date)
                        if today.day == current_month_date:
                            if line.day == today.day and line.month == month:
                                if leave.gende == 'male' or leave.gende =='female':
                                    employee_ids = self.env['hr.employee'].search([('gende','=',leave.gende),
                                                                                   ('employee_type','=',service_leave.tech_name),
                                                                                   ('state','=',emp_stages.tech_name),
                                                                                   ('active','=',True),
                                                                                   ])
                                elif leave.gende == 'transgender':
                                    employee_ids = self.env['hr.employee'].search([('employee_type','=',service_leave.tech_name),
                                                                                   ('state','=',emp_stages.tech_name),
                                                                                   ('active','=',True)
                                                                                   ])
                                for employee in employee_ids:
    #                                 print("@@@@@@@@@@@@@@@@@@@@@@@@",employee)
                                    if employee and not employee.leave_balance_id:
    #                                     print("ifffffffffffffffffffffffffff")
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
                                    elif employee and employee.leave_balance_id:
                                        for credit_policy in leave.creadit_policy_id:
                                            SQL = """
                                                       
                                                select he.id from 
                                                hr_employee as he
                                                left outer join hr_employee_leave_info as heli on heli.hr_employee_id = he.id
                                                left outer join hr_leave_type as hlt on hlt.id = heli.holiday_status_id
                                                where 
                                                he.id in (%s)
                                                and hlt.leave_type in (%s)
                                                and heli.leave_info = 'credit'
                                                and EXTRACT(DAY FROM heli.date) = '%s'
                                                    """
                                            self.env.cr.execute(SQL, (
                                                employee.id,
                                                leave.leave_type,
                                                credit_policy.day
                                            ))
                                            res = self.env.cr.fetchall()
    #                                         print("??????????????RESSSSSSSSSSSSSSSSSSSSS",res,today.day,today.strftime("%B"),credit_policy.day,credit_policy.month)
                                            if not res:
                                                if today.day == credit_policy.day and today.strftime("%B") == credit_policy.month:
    #                                                 print("#############################################")
                                                    allocate_leave = self.env['hr.leave.allocation'].create({'holiday_status_id': leave.id,
                                                                                                   'holiday_type': 'employee',
                                                                                                   'employee_id': employee.id,
                                                                                                   'number_of_days_display':line.no_pf_leaves_credit,
                                                                                                   'number_of_days':line.no_pf_leaves_credit,
                                                                                                   'name':'System Leave Allocation',
                                                                                                   'notes':'As Per Leave Policy'
                                                                                                   })
    #                                                 print("allocationnnnnnnnnnnnn",allocate_leave)
                                                    allocate_leave.sudo().action_approve()
                                                    
                                                    if allocate_leave:
                                                        leave_bal_id = self.env['hr.employee.leave.info'].create({
                                                                                                                'hr_employee_id':employee.id,
                                                                                                                'holiday_status_id':leave.id,
                                                                                                                'date':date.today(),
                                                                                                                'leave_info':'credit',
                                                                                                                'no_of_days':line.no_pf_leaves_credit
                                                                                                            })
                            
                
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
    