from odoo import models, fields, api,_
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class PfInterestDisbursement(models.Model):
    _name = 'pf.interest.disbursement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'pf.interest.disbursement'

    branch_id = fields.Many2many('res.branch', track_visibility='always')
    from_date = fields.Date('From Date', track_visibility='always')
    to_date = fields.Date('To Date', track_visibility='always')
    interest_rate = fields.Float('Interest Rate', track_visibility='always')


    @api.constrains('from_date','to_date','branch_id')
    @api.onchange('from_date','to_date','branch_id')
    def onchange_date_branch_gi(self):
        for rec in self:
            company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)], limit=1)
            if company:
                for com in company:
                    if rec.from_date and rec.to_date and rec.branch_id:
                        for line in com.pf_table:
                            if line.from_date >= rec.from_date and line.to_date <= rec.to_date:
                                rec.interest_rate = line.interest_rate


    @api.multi
    def button_submit(self):
        pass
        for rec in self:
            pf_details_ids = []
            employee_interest = 0
            company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)], limit=1)
            if company:
                for com in company:
                    if rec.from_date and rec.to_date and rec.branch_id:
                        for line in com.pf_table:
                            if line.from_date >= rec.from_date and line.to_date <= rec.to_date:
                                X = line.interest_rate

            from_date = rec.from_date
            to_date = rec.to_date
            X = 0.00

            pf_emp = self.env['pf.employee'].search([('employee_id.branch_id', 'in', rec.branch_id.ids)])
            for line in pf_emp:
                while from_date < rec.to_date:
                    # print('===============from date===================', from_date)
                    # print('===============To date===================', rec.to_date)
                    pay_rules = self.env['hr.payslip.line'].search(
                        [('slip_id.employee_id', '=', line.employee_id.id),
                         ('slip_id.state', '=', 'done'),
                         ('slip_id.date_from', '>=', from_date),
                         ('slip_id.date_to', '<', from_date + relativedelta(months=1)),
                         ('salary_rule_id.pf_register', '=', True),
                         ])
                    # print('=============Payslip===============', pay_rules)
                    emp = 0
                    volun = 0
                    emplyr = 0
                    employee_interest = 0
                    employer_contribution = 0
                    for ln in pay_rules:
                        if ln.salary_rule_id.pf_eve_type == 'employee':
                            emp += ln.total
                        elif ln.salary_rule_id.pf_eve_type == 'voluntary':
                            volun += ln.total
                        elif ln.salary_rule_id.pf_eve_type == 'employer':
                            emplyr += ln.total
                    # print('==================Employee===================', emp)
                    # print('==================Voluntary===================', volun)
                    # print('==================Employer===================', emplyr)
                    if str(from_date.month) == '1':
                        month = 'January'
                        employee_interest = (((emp + volun) * X) * 3) / 12
                        employer_contribution = (((emplyr) * X) * 3) / 12
                    elif str(from_date.month) == '2':
                        month = 'February'
                        employee_interest = (((emp + volun) * X) * 2) / 12
                        employer_contribution = (((emplyr) * X) * 2) / 12
                    elif str(from_date.month) == '3':
                        month = 'March'
                        employee_interest = (((emp + volun) * X) * 1) / 12
                        employer_contribution = (((emplyr) * X) * 1) / 12
                    elif str(from_date.month) == '4':
                        month = 'April'
                        employee_interest = (((emp + volun) * X) * 12) / 12
                        employer_contribution = (((emplyr) * X) * 12) / 12
                    elif str(from_date.month) == '5':
                        month = 'May'
                        employee_interest = (((emp + volun) * X) * 11) / 12
                        employer_contribution = (((emplyr) * X) * 11) / 12
                    elif str(from_date.month) == '6':
                        month = 'June'
                        employee_interest = (((emp + volun) * X) * 10) / 12
                        employer_contribution = (((emplyr) * X) * 10) / 12
                    elif str(from_date.month) == '7':
                        month = 'July'
                        employee_interest = (((emp + volun) * X) * 9) / 12
                        employer_contribution = (((emplyr) * X) * 9) / 12
                    elif str(from_date.month) == '8':
                        month = 'August'
                        employee_interest = (((emp + volun) * X) * 8) / 12
                        employer_contribution = (((emplyr) * X) * 8) / 12
                    elif str(from_date.month) == '9':
                        month = 'September'
                        employee_interest = (((emp + volun) * X) * 7) / 12
                        employer_contribution = (((emplyr) * X) * 7) / 12
                    elif str(from_date.month) == '10':
                        month = 'October'
                        employee_interest = (((emp + volun) * X) * 6) / 12
                        employer_contribution = (((emplyr) * X) * 6) / 12
                    elif str(from_date.month) == '11':
                        month = 'November'
                        employee_interest = (((emp + volun) * X) * 5) / 12
                        employer_contribution = (((emplyr) * X) * 5) / 12
                    elif str(from_date.month) == '12':
                        month = 'December'
                        employee_interest = (((emp + volun) * X) * 4) / 12
                        employer_contribution = (((emplyr) * X) * 4) / 12
                    else:
                        month = ''
                        employee_interest = 0
                        employer_contribution = 0
                    total = emp + volun + emplyr + employee_interest + employer_contribution
                    pf_details_ids.append((0, 0, {
                        'pf_details_id': line.id,
                        'employee_id': line.employee_id.id,
                        'type': ' Interest Deposit',
                        'pf_code': 'CEPF + VCPF',
                        'description': 'Interest on CEPF and VCPF',
                        'date': datetime.now().date(),
                        'amount': round(employee_interest),
                        'reference': 'Interest deposit on {}'.format(datetime.now().date()),
                    }))
                    from_date = from_date + relativedelta(months=1)
                line.pf_details_ids = pf_details_ids