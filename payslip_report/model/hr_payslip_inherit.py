from odoo import api, fields, models, tools , _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'   

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)

    @api.model
    def create(self, vals):
        res = super(HrPayslip, self).create(vals)
        payslip_ids = self.env['hr.payslip'].search([('employee_id','=',res.employee_id.id),
                                                     ('date_from','=',res.date_from),
                                                     ('date_to','=',res.date_to),
                                                     ('state','=','done')
                                                     ])
#         print("????????????????????????????",payslip_ids)
        if payslip_ids:
            raise ValidationError(_('You are Not Create Same Employee Payslip from Current Month'))
        else:
            return res


    def compute_difference_two_date(self):
        s=self.date_from
        e=self.date_to
        start = s.day
        end = e.day
        date_days = end - start + 1
        return date_days
    
    #added by sangita
    def compute_net_pay(self):
        loan_amount = 0.0
        if self.line_ids:
            for line in self.line_ids:
                if line.code == 'LOAN':
                    loan_amount = line.amount
                if line.code == 'NET':
                    net = line.amount - loan_amount
                    return net
    
#     def get_l_coming(self):
#         l_coming = 0.0
#         if self.line_ids:
#             for line in self.line_ids:
#                 if line.code == 'LC':
#                     l_coming = line.amount
#                     return l_coming
#                 
#     def half_h_deducation(self):
#         half_hour = 0.0
#         if self.line_ids:
#             for line in self.line_ids:
#                 if line.code == 'HHD':
#                     half_hour = line.amount
#                     print("?????????????????????????",half_hour)
#                     return half_hour
            
#     def half_day_deducation(self):
#         half_day = 0.0
#         if self.line_ids:
#             for line in self.line_ids:
#                 if line.code == 'HDD':
#                     half_day = line.amount
#                     print("____000000000000000000000000000000",half_day)
#                     return half_day
                
#     def early_going_days(self):
#         early_going = 0.0
#         if self.line_ids:
#             for line in self.line_ids:
#                 if line.code == 'EGD':
#                     early_going = line.amount
#                     return early_going
                
   
    @api.depends('line_ids.amount')
    def _compute_amount_total_words(self):
        for s in self:
            for line in s.line_ids:
                if line.code == 'NET':
                    s.amount_total_words = s.currency_id.amount_to_text(line.amount)

    amount_total_words = fields.Char("Total (In Words)", compute="_compute_amount_total_words",store=True)

    
    def leaves_type_cal_earned(self):
#         
        for leave in self:
            if leave.employee_id:
                print("///////////////////////////////////")
                SQL = """
                    
                select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Earned Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????",[i[0] for i in res])
                return r
            
    def leaves_type_cal_half_pay_leave(self):
#        
        for leave in self:
            if leave.employee_id:
#                 print("///////////////////////////////////",to_date)
                SQL = """
                   select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Half Pay Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????sick_leavessick_leaves",res)
                return r
    
    def leaves_type_cal_casual(self):
#        
        for leave in self:
            if leave.employee_id:
#                 print("///////////////////////////////////",to_date)
                SQL = """
                    select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Casual Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????casual_leavescasual_leaves",res)
                return r
            
    def leaves_type_cal_maternity(self):
#        
        for leave in self:
            if leave.employee_id:
#                 print("///////////////////////////////////",to_date)
                SQL = """
                    select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Maternity Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????casual_leavescasual_leaves",res)
                return r
            
    def leaves_type_cal_special_casual(self):
#        
        for leave in self:
            if leave.employee_id:
#                 print("///////////////////////////////////",to_date)
                SQL = """
                    select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Special Casual Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????casual_leavescasual_leaves",res)
                return r
            
    def leaves_type_cal_extra_ordinary_leave(self):
#        
        for leave in self:
            if leave.employee_id:
#                 print("///////////////////////////////////",to_date)
                SQL = """
                    select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Extra Ordinary Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????casual_leavescasual_leaves",res)
                return r
            
    def leaves_type_cal_paternity_leave(self):
#        
        for leave in self:
            if leave.employee_id:
#                 print("///////////////////////////////////",to_date)
                SQL = """
                    select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Paternity Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????casual_leavescasual_leaves",res)
                return r
            
    def leaves_type_cal_chlid_care_leave(self):
#        
        for leave in self:
            if leave.employee_id:
#                 print("///////////////////////////////////",to_date)
                SQL = """
                    select  sum(leave.number_of_days) as rem_leave
                    --leave.employee_id as employee
                    from hr_leave_report as leave
                    inner join hr_leave_type as hly on hly.id = leave.holiday_status_id
                    where leave.employee_id = %s and 
                    hly.leave_type = 'Child Care Leave' and
                    state not in ('refuse')
                    group by
                    leave.employee_id,
                    leave.holiday_status_id;
                """
                self.env.cr.execute(SQL,(
                                          leave.employee_id.id,
                                          ))
                res = self.env.cr.fetchall()
                r = [i[0] for i in res]
#                 print("??????????????????????casual_leavescasual_leaves",res)
                return r
    
    
    def unused_leaves_cal(self):
        unused = 0
        a = []
        unused_leaves_id = self.env['hr.leave'].search([('holiday_type','=','employee'),('employee_id','=',self.employee_id.id),('state','in',('confirm','validate'))])
        for i in unused_leaves_id:
            a += [i.number_of_days]
            unused = sum(a)
        return unused
    
    
    def used_leaves_cal(self):
        used = 0
        a = []
        used_leaves_id = self.env['hr.leave'].search([('holiday_type','=','employee'),('employee_id','=',self.employee_id.id), ('state','in',('confirm','validate'))])
        for i in used_leaves_id:
            a += [-i.number_of_days]
            used = sum(a)
        return used
    
    def get_late_coming_h(self):
        late_com_h = 0.0
        for s in self:
            attendance_ids = self.env['currated.attendance'].search([('employee_id','=',self.employee_id.id),('expected_start','>=',self.date_from),('expected_end','<=',self.date_to)])
#             print("???????/-?????????????????????????",attendance_ids)
            for attendance in attendance_ids:
                late_com_h = attendance.late_coming_min
                print("[[[[[[[[[[[[[[[[[[[[",late_com_h)
        return  late_com_h
    
class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'
    
    
    date_from = fields.Date(string='Date From', readonly=True)
    date_to = fields.Date(string='Date To', readonly=True) 
    state = fields.Selection([('draft', 'Draft'),
                        ('verify', 'Waiting'),
                        ('done', 'Done'),
                        ('cancel', 'Rejected')
                    ],string="Status",related="slip_id.state")  
    paid = fields.Boolean(string="Made Payment Order",related="slip_id.paid")
    date_from = fields.Date(string="Date From", related="slip_id.date_from")
    date_to = fields.Date(string="Date To", related="slip_id.date_to")
    payslip_batch = fields.Many2one(string="Payslip Batch",related="slip_id.payslip_run_id")
    current_month = fields.Selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
        ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')], readonly=True)

