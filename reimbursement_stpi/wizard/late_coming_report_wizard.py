from odoo import api, fields, models

# This will generate 16th of days
ROUNDING_FACTOR = 16

class WizardReimBursementReport(models.TransientModel):
    _name = 'reimbursement.report'
    _description = 'Reimbursement Report Wizard'
    
    
    # def get_tuple(self,tup):
    #     tup = tuple(tup)
    #     # print "666666666666555555555555555555555555555",tup
    #     if tup and len(tup) == 1:
    #         return '({0})'.format(tup[0])
    #     else:
    #         return tup
    
    # @api.onchange('date_range')
    # def get_dates(self):
    #     for s in self:
    #         if s.date_range:
    #             s.date_from = s.date_range.date_start
    #             s.date_to = s.date_range.date_end
                
    # date_range = fields.Many2one('date.range','Date range')
    # date_from = fields.Date(string="Date From",required=True)
    # date_to = fields.Date(string="Date To",required=True)
    
    
    # type = fields.Selection([('by_emp','Employee'),
    #                         ('by_dept','Department')
    #                         ],string="Type",default="by_emp")
    #
    # emp_ids = fields.Many2many('hr.employee',string="Employee")
    # dept_ids = fields.Many2many('hr.department',string="Department")
    
    report_of = fields.Selection([('reimbursement','Reimbursement')
                                  ], default='reimbursement', string="Report On")
    
    @api.multi
    def confirm_report(self):
        lst = []
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for employee in self.env['reimbursement'].browse(active_ids):
            # reim_repo = self.env['reimbursement.model.report'].create(
            #     {
            #         'reimbursement_sequence': employee.reimbursement_sequence,
            #         'employee_id': employee.employee_id.id,
            #         'name': employee.name,
            #         'job_id': employee.job_id.id,
            #         'department_id': employee.department_id.id,
            #         'branch_id': employee.branch_id.id,
            #         'birthday': employee.birthday,
            #         'state': 'draft',
            #     }
            # )
            lst.append(employee.id)
        # from_date = fields.Date.from_string(self.date_from)
        # to_date = fields.Date.from_string(self.date_to + timedelta(days=1))
        # print("??????????????????????????????????",to_date)
        if self.report_of == 'reimbursement':
            
            analysis_id=self.env['reimbursement.model.report'].search([])
            analysis_id.unlink()
            
            query = """ 
                insert into reimbursement_model_report (reimbursement_sequence,employee_id,job_id,branch_id,department_id,claimed_amount,net_amount,working_days,state)
    
                select ca.reimbursement_sequence,ca.employee_id,ca.job_id,ca.branch_id,ca.department_id,ca.claimed_amount,ca.net_amount,ca.working_days,ca.state
                from reimbursement as ca
                where
                ca.id in '{0}'
     
                """.format(lst)

            self.env.cr.execute(query)
            return {
                'name': 'Reimbursement Report',
                'view_type': 'form',
                'view_mode': 'tree,pivot',
                'res_model': 'reimbursement.model.report',
                'type': 'ir.actions.act_window',
                'target': 'current',
                }
    
    
    @api.multi
    def report_pdf(self):
        self.confirm_report()
        
        # report_id = self.env['ir.actions.report']
        # context = self.env.context
        #
        # if self.report_of == 'half_hr_deduction':
        #     report_id = self.env['ir.actions.report'].with_context(context).search(
        #         [('report_name', '=', 'curated_report.half_hr_deduction_report_template_id')], limit=1)
        #
        # elif self.report_of == 'half_day_deduction':
        #     report_id = self.env['ir.actions.report'].with_context(context).search(
        #         [('report_name', '=', 'curated_report.half_day_deduction_report_template_id')], limit=1)
        #
        # elif self.report_of == 'late_coming':
        #     report_id = self.env['ir.actions.report'].with_context(context).search(
        #         [('report_name', '=', 'curated_report.late_coming_template_id')], limit=1)
        #
        # elif self.report_of == 'early_going':
        #     report_id = self.env['ir.actions.report'].with_context(context).search(
        #         [('report_name', '=', 'curated_report.early_going_qa_report_print_action')], limit=1)
        #
        # elif self.report_of == 'overtime':
        #     report_id = self.env['ir.actions.report'].with_context(context).search(
        #         [('report_name', '=', 'curated_report.overtime_report_print_action')], limit=1)
        #
        # elif self.report_of == 'leave_without_pay':
        #     report_id = self.env['ir.actions.report'].with_context(context).search(
        #         [('report_name', '=', 'curated_report.leave_without_pay_print_action')], limit=1)
        #
        # if not report_id:
        #     raise UserError(
        #         _("Bad Report Reference") + _("This report is not loaded into the database: "))
        # print("--------------",report_id)
        #
        # return {
        #     'context': context,
        #     'type': 'ir.actions.report',
        #     'report_name': report_id.report_name,
        #     'report_type': report_id.report_type,
        #     'report_file': report_id.report_file,
        #     'name': report_id.name,
        #         }
        #
