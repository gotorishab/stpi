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
    _description = 'Recruitment'
    
    
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
                

    
    report_of = fields.Selection([('recruitment','Recruitment'),
                                  ],string="Report On")
    
    @api.multi
    def confirm_report(self):
        if self.report_of == 'recruitment':
            
            analysis_id=self.env['recruitment.report'].search([])
            analysis_id.unlink()
            
            query = """ 
                insert into recruitment_report (x_jobposition,x_department,x_branch,x_sanctionedpositions,
                x_currentempcount,x_scpercet,x_stpercet,x_obcpercet,x_ebcpercet,x_vhpercent,x_phpercent,
                x_hhpercent,x_ruleclass,x_nosc,x_nost,x_noobc,x_noebc,x_currobc,x_currgen,x_currsc,x_currst,x_currewc)
    
               select hj.name as x_jobposition,
               	hd.name as x_department,
               	rb.name as x_branch,
                sanctionedpost as x_sanctionedpositions,
                (select count(*) from hr_employee where hr_employee.job_id = hj.id) as x_currentempcount,
                case
                when hj.jp = True then hj.scpercent
                else rc.scpercent
                end as x_scpercet,
                case
                when hj.jp = True then hj.stpercent
                else rc.stpercent
                end as x_stpercet,
                case
                when hj.jp = True then hj.obcercent
                else rc.obcercent
                end as x_obcpercet,
                case
                when hj.jp = True then hj.ebcpercent
                else rc.ebcpercent
                end as x_ebcpercet,
                case
                when hj.jp = True then hj.vhpercent
                else rc.vhpercent
                end as x_vhpercent,
                case
                when hj.jp = True then hj.phpercent
                else rc.phpercent
                end as x_phpercent,
                case
                when hj.jp = True then hj.hhpercent
                else rc.hhpercent
                end as x_hhpercent,
                case
                when hj.jp = True then 'Job Position Specific'
                else 'Global Rule'
                end as x_ruleclass,
                case
                when hj.jp = True then hj.scpercent*sanctionedpost/100
                else rc.scpercent*sanctionedpost/100
                end as x_nosc,
                case
                when hj.jp = True then hj.stpercent*sanctionedpost/100
                else rc.scpercent*sanctionedpost/100
                end as x_nost,
                case
                when hj.jp = True then hj.obcercent*sanctionedpost/100
                else rc.obcercent*sanctionedpost/100
                end as x_noobc,
                case
                when hj.jp = True then hj.ebcpercent*sanctionedpost/100
                else rc.ebcpercent*sanctionedpost/100
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

