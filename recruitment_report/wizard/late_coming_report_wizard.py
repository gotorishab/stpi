from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta
import datetime
from odoo.tools import float_utils
from collections import defaultdict
from pytz import utc

# This will generate 16th of days
ROUNDING_FACTOR = 16

class WizardLateComing(models.TransientModel):
    _name = 'wizard.recruitment'
    _description = 'Late Coming Wizard'
    
    
    def get_tuple(self,tup):
        tup = tuple(tup)
        # print "666666666666555555555555555555555555555",tup
        if tup and len(tup) == 1:
            return '({0})'.format(tup[0])
        else:
            return tup
    
    @api.onchange('date_range')
    def get_dates(self):
        for s in self:
            if s.date_range:
                s.date_from = s.date_range.date_start
                s.date_to = s.date_range.date_end
                
    date_range = fields.Many2one('date.range','Date range')
    date_from = fields.Date(string="Date From",required=True)
    date_to = fields.Date(string="Date To",required=True)
    
    
    type = fields.Selection([('by_emp','Employee'),
                            ('by_dept','Department')
                            ],string="Type",default="by_emp")
    
    emp_ids = fields.Many2many('hr.employee',string="Employee")
    dept_ids = fields.Many2many('hr.department',string="Department")
    
    report_of = fields.Selection([('recruitment','Late Coming Report'),
                                  ('half_hr_deduction','Half Hour Deduction Report'),
                                  ('half_day_deduction','Half Day Deduction Report'),
                                  ('early_going','Early Going'),
                                  ('overtime','Overtime'),
                                  ('leave_without_pay','Leave Without Pay'),
                                  ('lwp_exception','LWP Exception')
                                  ],string="Report On")
    
    @api.multi
    def confirm_report(self):
        from_date = fields.Date.from_string(self.date_from)
        to_date = fields.Date.from_string(self.date_to + timedelta(days=1))
        print("??????????????????????????????????",to_date)
        if self.report_of == 'recruitment':
            
            analysis_id=self.env['recruitment.report'].search([])
            analysis_id.unlink()
            
            query = """ 
                insert into recruitment_report (emp_code,emp_name,dept_id,check_in,check_out,duty_hr,actual_duty_hr,recruitment_min,roster_id,emp_id)
    
               select hj.name as x_jobposition,
	hd.name as x_department,
	rb.name as x_branch,
	sanctionedpost as x_sanctionedpositions,
	(select count(*) from hr_employee where hr_employee.job_id = hj.id) as x_currentempcount,
	case
	when hj.x_breakup = True then hj.x_sc
	else rc.x_csc
	end as x_scpercet,
	case
	when hj.x_breakup = True then x_st
	else rc.x_sc
	end as x_stpercet,
	case
	when hj.x_breakup = True then hj.x_obc
	else rc.x_obc
	end as x_obcpercet,
	case
	when hj.x_breakup = True then x_ebs
	else x_cecs
	end as x_ebcpercet,
	case
	when hj.x_breakup = True then x_vh
	else x_cvh
	end as x_vhpercent,
	case
	when hj.x_breakup = True then x_ph
	else x_cph
	end as x_phpercent,
	case
	when hj.x_breakup = True then x_hh
	else x_chh
	end as x_hhpercent,
	case
	when hj.x_breakup = True then 'Job Position Specific'
	else 'Global Rule'
	end as x_ruleclass,
	case
	when hj.x_breakup = True then hj.x_sc*sanctionedpost/100
	else rc.x_csc*sanctionedpost/100
	end as x_nosc,
	case
	when hj.x_breakup = True then x_st*sanctionedpost/100
	else rc.x_sc*sanctionedpost/100
	end as x_nost,
	case
	when hj.x_breakup = True then hj.x_obc*sanctionedpost/100
	else rc.x_obc*sanctionedpost/100
	end as x_noobc,
	case
	when hj.x_breakup = True then x_ebs*sanctionedpost/100
	else x_cecs*sanctionedpost/100
	end as x_noebc,
	(select count(*) from hr_employee as he,employee_religion as er where er.name = 'OBC' and he.job_id = hj.id) as x_currobc,
	(select count(*) from hr_employee as he,employee_religion as er where er.name = 'General' and he.job_id = hj.id) as x_currgen,
	(select count(*) from hr_employee as he,employee_religion as er where er.name = 'SC' and he.job_id = hj.id) as x_currsc,
	(select count(*) from hr_employee as he,employee_religion as er where er.name = 'ST' and he.job_id = hj.id) as x_currst,
	(select count(*) from hr_employee as he,employee_religion as er where er.name = 'EWC' and he.job_id = hj.id) as x_currewc

from hr_job as hj
inner join res_company as rc on rc.id=hj.company_id
left outer join hr_department as hd on hd.id=hj.department_id
left outer join res_branch as rb on rb.id=hj.branch_id
                
                """

            self.env.cr.execute(query)
            return {
                'name': 'Roster Report',
                'view_type': 'form',
                'view_mode': 'tree,pivot',
                'res_model': 'recruitment.report',
                'type': 'ir.actions.act_window',
                'target': 'current',
                }

    
    @api.multi
    def report_pdf(self):
        self.confirm_report()
        
        report_id = self.env['ir.actions.report']
        context = self.env.context

        if self.report_of == 'recruitment':
            report_id = self.env['ir.actions.report'].with_context(context).search(
                [('report_name', '=', 'recruitment_report.recruitment_template_id')], limit=1)

        if not report_id:
            raise UserError(
                _("Bad Report Reference") + _("This report is not loaded into the database: "))
        print("--------------",report_id)
        
        return {
            'context': context,
            'type': 'ir.actions.report',
            'report_name': report_id.report_name,
            'report_type': report_id.report_type,
            'report_file': report_id.report_file,
            'name': report_id.name,
                }

