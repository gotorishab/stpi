from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import time, datetime,timedelta
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date, datetime
import datetime
from odoo.tools import float_utils
from collections import defaultdict
from pytz import utc


class WizardLateComing(models.TransientModel):
    _name = 'pf.ledger.wizard'
    _description = 'PF Ledger'
    

    @api.onchange('employee_id')
    def get_branch_job(self):
        for rec in self:
            rec.branch_id = rec.employee_id.branch_id
            rec.job_id = rec.employee_id.job_id

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    
    report_of = fields.Selection([('pf_ledger','PF Ledger'),
                                  ],string="Report On", default='pf_ledger')
    employee_id = fields.Many2one('hr.employee','Requested By', default=_default_employee)
    interest_rate = fields.Float('Interest Rate')
    ledger_for_year = fields.Many2one('date.range', string='Ledger for the year')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    branch_id = fields.Many2one('res.branch', string='Branch')
    job_id = fields.Many2one('hr.job', string='Functional Designation')




    @api.onchange('branch_id','ledger_for_year')
    @api.constrains('branch_id','ledger_for_year')
    def check_existing_branch_sr(self):
        self.from_date = self.ledger_for_year.date_start
        self.to_date = self.ledger_for_year.date_end
        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)], limit=1)
        if company:
            for com in company:
                if self.ledger_for_year.date_start and self.ledger_for_year.date_end and self.branch_id:
                    for line in com.pf_table:
                        if line.from_date >= self.ledger_for_year.date_start and line.to_date <= self.ledger_for_year.date_end:
                            self.interest_rate = line.interest_rate



    @api.multi
    def confirm_report(self):
        for rec in self:
            X = rec.interest_rate
            print('=============X===============', X)
            dr = self.env['pf.ledger.report'].search([('employee_id', '=', rec.employee_id.id),('ledger_for_year', '=', rec.ledger_for_year.id)])
            for lines in dr:
                lines.unlink()

            pay_rules_old = self.env['pf.employee.details'].search(
                    [('pf_details_id.employee_id', '=', rec.employee_id.id),
                     ('date', '<', rec.ledger_for_year.date_start)
                     ])
            total = 0.00
            for ln in pay_rules_old:
                if ln.type == 'Deposit':
                    total += ln.amount
                else:
                    total -= ln.amount
            cr_lines = self.env['pf.ledger.report'].create({
                'employee_id': rec.employee_id.id,
                'ledger_for_year': rec.ledger_for_year.id,
                'branch_id': rec.employee_id.branch_id.id,
                'month': 'Opening',
                'epmloyee_contribution': ' ',
                'voluntary_contribution': ' ',
                'employer_contribution': ' ',
                'interest_employee_voluntary': ' ',
                'interest_employer': ' ',
                'total': str(round(total)),
            })



            pay_rules = self.env['pf.employee.details'].search(
                    [('pf_details_id.employee_id', '=', rec.employee_id.id),
                     ('date', '>=', rec.ledger_for_year.date_start),
                     ('date', '<=', rec.ledger_for_year.date_end)
                     ])
            print('=============lines===============',pay_rules)
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'January'
            for ln in pay_rules:
                if str(ln.date.month) == '1':
                    month = 'January'
                    employee_interest = (((emp + volun) * X) * 3) / 12
                    employer_contribution = (((emplyr) * X) * 3) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            jan = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'February'
            for ln in pay_rules:
                if str(ln.date.month) == '2':
                    month = 'February'
                    employee_interest = (((emp + volun) * X) * 2) / 12
                    employer_contribution = (((emplyr) * X) * 2) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            feb = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'March'
            for ln in pay_rules:
                if str(ln.date.month) == '3':
                    month = 'March'
                    employee_interest = (((emp + volun) * X) * 1) / 12
                    employer_contribution = (((emplyr) * X) * 1) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            mar = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'April'
            for ln in pay_rules:
                if str(ln.date.month) == '4':
                    month = 'April'
                    employee_interest = (((emp + volun) * X) * 12) / 12
                    employer_contribution = (((emplyr) * X) * 12) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            apr = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'May'
            for ln in pay_rules:
                if str(ln.date.month) == '5':
                    month = 'May'
                    employee_interest = (((emp + volun) * X) * 11) / 12
                    employer_contribution = (((emplyr) * X) * 11) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            may = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'June'
            for ln in pay_rules:
                if str(ln.date.month) == '6':
                    month = 'June'
                    employee_interest = (((emp + volun) * X) * 10) / 12
                    employer_contribution = (((emplyr) * X) * 10) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            jun = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'July'
            for ln in pay_rules:
                if str(ln.date.month) == '7':
                    month = 'July'
                    employee_interest = (((emp + volun) * X) * 9) / 12
                    employer_contribution = (((emplyr) * X) * 9) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            jul = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'August'
            for ln in pay_rules:
                if str(ln.date.month) == '8':
                    month = 'August'
                    employee_interest = (((emp + volun) * X) * 8) / 12
                    employer_contribution = (((emplyr) * X) * 8) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            aug = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'September'
            for ln in pay_rules:
                if str(ln.date.month) == '9':
                    month = 'September'
                    employee_interest = (((emp + volun) * X) * 7) / 12
                    employer_contribution = (((emplyr) * X) * 7) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            sept = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'October'
            for ln in pay_rules:
                if str(ln.date.month) == '10':
                    month = 'October'
                    employee_interest = (((emp + volun) * X) * 6) / 12
                    employer_contribution = (((emplyr) * X) * 6) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            oct = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            

            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'November'
            for ln in pay_rules:
                if str(ln.date.month) == '11':
                    month = 'November'
                    employee_interest = (((emp + volun) * X) * 5) / 12
                    employer_contribution = (((emplyr) * X) * 5) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            nov = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            
            
            emp = 0
            volun = 0
            emplyr = 0
            employee_interest = 0
            employer_contribution = 0
            month = 'December'
            for ln in pay_rules:
                if str(ln.date.month) == '12':
                    month = 'December'
                    employee_interest = (((emp + volun) * X) * 4) / 12
                    employer_contribution = (((emplyr) * X) * 4) / 12
                    if ln.pf_code == 'CPF':
                        if ln.type == 'Deposit':
                            emp += ln.amount
                        else:
                            emp -= ln.amount
                    elif ln.pf_code == 'VCPF':
                        if ln.type == 'Deposit':
                            volun += ln.amount
                        else:
                            volun -= ln.amount
                    elif ln.pf_code == 'CEPF':
                        if ln.type == 'Deposit':
                            emplyr += ln.amount
                        else:
                            emplyr -= ln.amount
            total = emp + volun + emplyr + employee_interest + employer_contribution
            dec = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': str(month),
                    'epmloyee_contribution': str(round(emp)),
                    'voluntary_contribution': str(round(volun)),
                    'employer_contribution': str(round(emplyr)),
                    'interest_employee_voluntary': str(round(employee_interest)),
                    'interest_employer': str(round(employer_contribution)),
                    'total': str(round(total)),
                })
            #print('================creation lines================', cr_lines)
            
            clos_bal = self.env['pf.ledger.report'].create({
                    'employee_id': rec.employee_id.id,
                    'ledger_for_year': rec.ledger_for_year.id,
                    'branch_id': rec.employee_id.branch_id.id,
                    'month': 'Closing',
                    'epmloyee_contribution': str(int(jan.epmloyee_contribution) + int(feb.epmloyee_contribution) + int(mar.epmloyee_contribution) + int(apr.epmloyee_contribution) + int(may.epmloyee_contribution) + int(jun.epmloyee_contribution) + int(jul.epmloyee_contribution) + int(aug.epmloyee_contribution) + int(sept.epmloyee_contribution) + int(oct.epmloyee_contribution) + int(nov.epmloyee_contribution) + int(dec.epmloyee_contribution)),
                    'voluntary_contribution': str(int(jan.voluntary_contribution) + int(feb.voluntary_contribution) + int(mar.voluntary_contribution) + int(apr.voluntary_contribution) + int(may.voluntary_contribution) + int(jun.voluntary_contribution) + int(jul.voluntary_contribution) + int(aug.voluntary_contribution) + int(sept.voluntary_contribution) + int(oct.voluntary_contribution) + int(nov.voluntary_contribution) + int(dec.voluntary_contribution)),
                    'employer_contribution': str(int(jan.employer_contribution) + int(feb.employer_contribution) + int(mar.employer_contribution) + int(apr.employer_contribution) + int(may.employer_contribution) + int(jun.employer_contribution) + int(jul.employer_contribution) + int(aug.employer_contribution) + int(sept.employer_contribution) + int(oct.employer_contribution) + int(nov.employer_contribution) + int(dec.employer_contribution)),
                    'interest_employee_voluntary': str(int(jan.interest_employee_voluntary) + int(feb.interest_employee_voluntary) + int(mar.interest_employee_voluntary) + int(apr.interest_employee_voluntary) + int(may.interest_employee_voluntary) + int(jun.interest_employee_voluntary) + int(jul.interest_employee_voluntary) + int(aug.interest_employee_voluntary) + int(sept.interest_employee_voluntary) + int(oct.interest_employee_voluntary) + int(nov.interest_employee_voluntary) + int(dec.interest_employee_voluntary)),
                    'interest_employer': str(int(jan.interest_employer) + int(feb.interest_employer) + int(mar.interest_employer) + int(apr.interest_employer) + int(may.interest_employer) + int(jun.interest_employer) + int(jul.interest_employer) + int(aug.interest_employer) + int(sept.interest_employer) + int(oct.interest_employer) + int(nov.interest_employer) + int(dec.interest_employer)),
                    'total': str(int(jan.total) + int(feb.total) + int(mar.total) + int(apr.total) + int(may.total) + int(jun.total) + int(jul.total) + int(aug.total) + int(sept.total) + int(oct.total) + int(nov.total) + int(dec.total)),
                })
            #print('================creation lines================', cr_lines)

            return {
                'name': 'PF Ledger',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'pf.ledger.report',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('employee_id', '=', rec.employee_id.id),('ledger_for_year', '=', rec.ledger_for_year.id)]
            }