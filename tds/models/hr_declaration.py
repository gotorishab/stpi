from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta

class HrDeclaration(models.Model):
    _name = 'hr.declaration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'HR Declaration'


    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    @api.multi
    @api.depends('slab_ids','med_ins_ids','deduction_saving_ids','tax_home_ids','tax_education_ids','rgess_ids','dedmedical_ids','dedmedical_self_ids')
    def _compute_allowed_rebate(self):
        for rec in self:
            total_approved = 0.0
            total_app = 0.00
            max_allowed_approved = 0.00
            max_allowed_app = 0.00
            for line in rec.slab_ids:
                if line.it_rule == '80_c' or line.it_rule == '80ccd1':
                    total_approved += line.investment
                    max_allowed_approved += line.saving_master.rebate
                if line.it_rule == '80ccd1b':
                    total_app += line.investment
                    max_allowed_app += line.saving_master.rebate
            if total_approved <= max_allowed_approved:
                rec.allowed_rebate_under_80c = total_approved
            else:
                rec.allowed_rebate_under_80c = max_allowed_approved
            if total_app <= max_allowed_app:
                rec.allowed_rebate_under_80b = total_app
            else:
                rec.allowed_rebate_under_80b = max_allowed_app
            total_dd = 0.00
            max_allowed_dd = 0.00
            for line in rec.med_ins_ids:
                if line.it_rule == '80d':
                    total_dd += line.investment
                    max_allowed_dd += line.saving_master.rebate
            if total_dd <= max_allowed_dd:
                rec.allowed_rebate_under_80d = total_dd
            else:
                rec.allowed_rebate_under_80d = max_allowed_dd
            total_dsa = 0.00
            max_allowed_dsa = 0.00
            for line in rec.deduction_saving_ids:
                if line.it_rule:
                    total_dsa += line.investment
                    max_allowed_dsa += line.saving_master.rebate
            if total_dsa <= max_allowed_dsa:
                rec.allowed_rebate_under_80dsa = total_dsa
            else:
                rec.allowed_rebate_under_80dsa = max_allowed_dsa
            total_tbhl = 0.00
            total_ee = 0.00
            total_24 = 0.00
            max_allowed_ee = 0.00
            max_allowed_24 = 0.00
            max_allowed_tbhl = 0.00
            for line in rec.tax_home_ids:
                if line.it_rule == '80ee':
                    total_ee += line.investment
                    max_allowed_ee += line.saving_master.rebate
                elif line.it_rule == '24':
                    total_24 += line.investment
                    max_allowed_24 += line.saving_master.rebate
                else:
                    total_tbhl += line.investment
                    max_allowed_tbhl += line.saving_master.rebate
            if total_ee <= max_allowed_ee:
                rec.allowed_rebate_under_80ee = total_ee
            else:
                rec.allowed_rebate_under_80ee = max_allowed_ee
            if total_24 <= max_allowed_24:
                rec.allowed_rebate_under_24 = total_24
            else:
                rec.allowed_rebate_under_24 = max_allowed_24
            if total_tbhl <= max_allowed_tbhl:
                rec.allowed_rebate_under_tbhl = total_tbhl
            else:
                rec.allowed_rebate_under_tbhl = max_allowed_tbhl
            total_tei = 0.00
            max_allowed_tei = 0.00
            for line in rec.tax_education_ids:
                if line.it_rule:
                    total_tei += line.investment
                    max_allowed_tei += line.saving_master.rebate
            if total_tei <= max_allowed_tei:
                rec.allowed_rebate_under_80e = total_tei
            else:
                rec.allowed_rebate_under_80e = max_allowed_tei

            total_80ccg = 0.00
            max_allowed_80ccg = 0.00
            for line in rec.rgess_ids:
                if line.it_rule:
                    total_80ccg += line.investment
                    max_allowed_80ccg += line.saving_master.rebate
            if total_80ccg <= max_allowed_80ccg:
                rec.allowed_rebate_under_80ccg = total_80ccg
            else:
                rec.allowed_rebate_under_80ccg = max_allowed_80ccg
            total_80dd = 0.00
            max_allowed_80dd = 0.00
            for line in rec.dedmedical_ids:
                if line.it_rule:
                    total_80dd += line.investment
                    max_allowed_80dd += line.saving_master.rebate
            if total_80dd <= max_allowed_80dd:
                rec.allowed_rebate_under_80cdd = total_80dd
            else:
                rec.allowed_rebate_under_80cdd = max_allowed_80dd
            total_80mesdr = 0.00
            max_allowed_80mesdr = 0.00
            for line in rec.dedmedical_self_ids:
                if line.it_rule:
                    total_80mesdr += line.investment
                    max_allowed_80mesdr += line.saving_master.rebate
            if total_80mesdr <= max_allowed_80mesdr:
                rec.allowed_rebate_under_80mesdr = total_80mesdr
            else:
                rec.allowed_rebate_under_80mesdr = max_allowed_80mesdr


    @api.multi
    @api.depends('rent_paid_ids')
    def compute_rent_lines(self):
        for rec in self:
            sum = 0
            for lines in rec.rent_paid_ids:
                sum += lines.amount
            rec.rent_paid = sum


    @api.multi
    @api.depends('employee_id','date_range')
    def _compute_bda_salary(self):
        for rec in self:
            bs = 0.00
            da = 0.00
            prl_id = self.env['hr.payslip.line'].sudo().search([('slip_id.employee_id', '=', rec.employee_id.id),('slip_id.state', '=', 'done'),('slip_id.date_from', '>', rec.date_range.date_start),('slip_id.date_to', '<', rec.date_range.date_end)])
            for pr in prl_id:
                if pr.code == 'BASIC':
                    bs += pr.amount
                elif pr.code == 'DA':
                    da += pr.amount
            rec.basic_salary = bs
            rec.da_salary = da



    employee_id = fields.Many2one('hr.employee', string='Requeested By', default=_default_employee, track_visibility='always')
    job_id = fields.Many2one('hr.job', string="Functional Designation", store=True, track_visibility='always')
    branch_id = fields.Many2one('res.branch', string="Branch", store=True, track_visibility='always')
    department_id = fields.Many2one('hr.department', string="Department", store=True, track_visibility='always')
    date_range = fields.Many2one('date.range','Financial Year', track_visibility='always')
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True, track_visibility='always')
    rent_paid_ids = fields.One2many('rent.paid', 'rent_paid_id', string='Rent Paid')
    rent_paid = fields.Float(string='Rent Paid', compute='compute_rent_lines')
    tax_salary_final = fields.Float(string='Gross Salary', store=True, track_visibility='always')
    forecast_gross = fields.Float(string='Forecast Gross')
    basic_salary = fields.Float(string='Basic Salary', compute='_compute_bda_salary')
    da_salary = fields.Float(string='DA', compute='_compute_bda_salary')
    total_tds_paid = fields.Float(string='Total TDS Paid')
    previous_employer_income = fields.Float(string='Previous Employer Income')
    income_after_exemption = fields.Float(string='Income after Exemption')
    income_after_std_ded = fields.Float(string='Income after Std. Deduction')
    income_after_pro_tax = fields.Float(string='Income after Professional Tax')
    taxable_income = fields.Float(string='Taxable Income')

    exemption_ids = fields.One2many('declaration.exemption', 'exemption_id', string='Exemption Ids')
    std_ded_ids = fields.One2many('declaration.standard', 'std_ded_id', string='Exemption Ids')
    rebate_ids = fields.One2many('declaration.rebate', 'rebate_id', string='Rebate Ids')
    slab_ids = fields.One2many('declaration.slab', 'slab_id', string='Slab 80 Ids')
    hra_ids = fields.One2many('declaration.hra', 'hra_id', string='HRA - House Rent Allowances ')
    med_ins_ids = fields.One2many('declaration.medical', 'med_ins_id', string='Medical Insurance Premium paid ')
    deduction_saving_ids = fields.One2many('declaration.deduction', 'deduction_saving_id', string='Deductions on Interest on Savings Account')
    tax_home_ids = fields.One2many('declaration.taxhome', 'tax_home_id', string='Tax Benefits on Home Loan')
    tax_education_ids = fields.One2many('declaration.taxeducation', 'tax_education_id', string='Tax benefit on Education Loan (80E)')
    rgess_ids = fields.One2many('declaration.rgess', 'rgess_id', string='Deductions on Rajiv Gandhi Equity Saving Scheme')
    dedmedical_ids = fields.One2many('declaration.dedmedical', 'dedmedical_id', string='Deductions on Medical Expenditure for a Handicapped Relative')
    dedmedical_self_ids = fields.One2many('declaration.dedmedicalself', 'dedmedical_self_id', string='Deductions on Medical Expenditure on Self or Dependent Relative')
    # net_allowed_rebate = fields.Float('Net Allowed Rebate', compute='compute_net_allowed_rebate')
    # income_after_rebate = fields.Float('Income after Rebate')
    tax_payable = fields.Float('Tax Payable')
    tax_payable_zero = fields.Boolean('Tax Payable greater than equal to zero')
    tax_computed_bool = fields.Boolean('Tax computed bool', default = False)
    tax_payment_ids = fields.One2many('tax.payment','tax_payment_id', string='Tax Payment')
    allowed_rebate_under_80c = fields.Float(string='Allowed Rebate under Section 80', compute='_compute_allowed_rebate')
    allowed_rebate_under_80b = fields.Float(string='Allowed Rebate under Section 80CCD1(B)', compute='_compute_allowed_rebate')
    allowed_rebate_under_80d = fields.Float(string='Allowed Rebate under Section 80D', compute='_compute_allowed_rebate')
    allowed_rebate_under_80dsa = fields.Float(string='Allowed Rebate under Interest on Savings Account', compute='_compute_allowed_rebate')
    allowed_rebate_under_tbhl = fields.Float(string='Allowed Rebate under Tax Benefits on Home Loan', compute='_compute_allowed_rebate')

    allowed_rebate_under_80ee = fields.Float(string='Allowed Rebate under Section 80 EE', compute='_compute_allowed_rebate')
    allowed_rebate_under_24 = fields.Float(string='Allowed Rebate under Section 24', compute='_compute_allowed_rebate')


    allowed_rebate_under_80e = fields.Float(string='Allowed Rebate under Section 80 E', compute='_compute_allowed_rebate')
    allowed_rebate_under_80ccg = fields.Float(string='Allowed Rebate under Section 80 CCG', compute='_compute_allowed_rebate')
    allowed_rebate_under_80cdd = fields.Float(string='Allowed Rebate under Section 80 DD', compute='_compute_allowed_rebate')
    allowed_rebate_under_80mesdr = fields.Float(string='Allowed Rebate under Medical Expenditure on Self or Dependent Relative', compute='_compute_allowed_rebate')


    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('verified', 'Verified')
         ], required=True, default='draft', string='Status', track_visibility='always')


    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_emo_get_basic(self):
        for record in self:
            record.job_id = record.employee_id.job_id
            record.branch_id = record.employee_id.branch_id
            record.department_id = record.employee_id.department_id

    #
    # @api.depends('exemption_ids','rebate_ids','allowed_rebate_under_80c','allowed_rebate_under_80b','allowed_rebate_under_80d','allowed_rebate_under_80dsa','allowed_rebate_under_80e','allowed_rebate_under_80ccg','allowed_rebate_under_tbhl','allowed_rebate_under_80ee','allowed_rebate_under_24','allowed_rebate_under_80cdd', 'allowed_rebate_under_80mesdr')
    # def compute_net_allowed_rebate(self):
    #     for rec in self:
    #         sum=0.00
    #         sum1 = 0.00
    #         for de in rec.exemption_ids:
    #             sum+=de.allowed_rebate
    #         for de in rec.rebate_ids:
    #             sum+=de.allowed_rebate
    #         sum1 = rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr
    #         rec.net_allowed_rebate = sum + sum1




    @api.multi
    @api.depends('employee_id')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            if record.employee_id:
                name = str(record.employee_id.name) + ' - HR Declaration'
            else:
                name = 'HR Declaration'
            res.append((record.id, name))
        return res


    @api.multi
    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'to_approve'})

    @api.multi
    def button_forecast_gross(self):
        for rec in self:
            sum = 0
            proll = self.env['hr.payslip.line'].sudo().search([('slip_id.employee_id', '=', rec.employee_id.id),
                                                        ('slip_id.state', '=', 'done'),
                                                       ('code', '=', 'NET'),
                                                        ('slip_id.date_to', '>', rec.date_range.date_start),
                                                    ], limit=1)
            for pr in proll:
                rec.forecast_gross = pr.amount*12

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        self.ensure_one()
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        ctx = dict(
            default_composition_mode='comment',
            default_res_id=self.id,

            default_model='hr.declaration',
            default_is_log='True',
            custom_layout='mail.mail_notification_light'
        )
        mw = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        self.write({'state': 'draft'})
        return mw


    @api.multi
    def button_compute_tax(self):
        for rec in self:
            sum = 0
            dstart = rec.date_range.date_start - relativedelta(months=1)
            dend = rec.date_range.date_end + relativedelta(months=1)
            proll =  self.env['hr.payslip.line'].sudo().search([('slip_id.employee_id', '=', rec.employee_id.id),
                                                         ('slip_id.state', '=', 'done'),
                                                         ('salary_rule_id.taxable_percentage', '>', 0),
                                                         ('slip_id.date_from', '>=', dstart),
                                                         ('slip_id.date_to', '<=', dend)])
            for i in proll:
                sum += i.taxable_amount
            rec.tax_salary_final = sum
            # rec.income_after_rebate = rec.tax_salary_final - rec.net_allowed_rebate
            age = 0
            if rec.employee_id.birthday:
                age = ((datetime.now().date() - rec.employee_id.birthday).days) / 365

            inc_tax_slab =  self.env['income.tax.slab'].sudo().search([('salary_from', '<=', rec.tax_salary_final),
                                                                ('salary_to', '>=', rec.tax_salary_final),
                                                                ('age_from', '<=', age),
                                                                ('age_to', '>=', age)],order ="create_date desc",
                                                               limit=1)
            for tax_slab in inc_tax_slab:
                t1 = (tax_slab.tax_rate * (rec.tax_salary_final/100))
                t2 = (t1 * (1 + tax_slab.surcharge / 100))
                t3 = (t2 * (1 + tax_slab.cess / 100))
                rec.tax_payable = t3
            if rec.tax_payable <= 0.00:
                rec.tax_payable_zero = False
                rec.tax_payable = 0.00
            else:
                rec.tax_payable_zero = True
            rec.std_ded_ids.unlink()
            rec.exemption_ids.unlink()
            rec.rebate_ids.unlink()
            rec.slab_ids.unlink()
            ex_std_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Std. Deduction'), ('it_rule', '=', 'mus10ale')], limit=1)
            my_investment = 0.00
            if ex_std_id:
                my_investment = 0.00
                my_allowed_rebate = 0.00
                if rec.tax_salary_final >= ex_std_id.rebate:
                    my_investment = ex_std_id.rebate
                else:
                    my_investment = rec.tax_salary_final

                if my_investment <= ex_std_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_std_id.rebate
                self.env['declaration.standard'].create({
                    'std_ded_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_std_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_child_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Child Education Allowance & Hostel Expenditure Allowance'), ('it_rule', '=', 'mus10ale')], limit=1)
            child_id = self.env['employee.relative'].sudo().search(
                [('employee_id', '=', rec.employee_id.id)])
            count = 0
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in child_id:
                if cc.relate_type_name == 'Son' or cc.relate_type_name == 'Daughter':
                    count+=1
            if ex_child_id:
                if rec.employee_id.date_of_join and rec.date_range.date_start < rec.employee_id.date_of_join <= rec.date_range.date_end:
                    nm = ((rec.date_range.date_end - rec.employee_id.date_of_join).days)/30
                    my_investment = count * 100 * nm
                else:
                    my_investment = count * 100 * 12
                if my_investment <= ex_child_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_child_id.rebate

                self.env['declaration.exemption'].create({
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_child_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_hra_id = self.env['saving.master'].sudo().search([('saving_type', '=', 'HRA Exemption'), ('it_rule', '=', 'mus10ale')], limit=1)
            prl_id = self.env['hr.payslip.line'].sudo().search([('slip_id.employee_id', '=', rec.employee_id.id),('slip_id.state', '=', 'done'),('code', '=', 'HRA'),('slip_id.date_from', '>', rec.date_range.date_start),('slip_id.date_to', '<', rec.date_range.date_end)])
            sum_bs = 0.00
            sum_rent = 0.00
            sum_prl = 0.00
            sum=0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in prl_id:
                sum_prl+=cc.amount
            if rec.employee_id.address_home_id.city_id.metro == True:
                sum_bs = ((rec.basic_salary + rec.da_salary)*50)/100
            else:
                sum_bs = ((rec.basic_salary + rec.da_salary)*40)/100
            sum_rent = rec.rent_paid - ((rec.basic_salary + rec.da_salary)*10)/100
            if sum_prl <= sum_bs and sum_prl <= sum_rent:
                sum = sum_prl
            elif sum_bs <= sum_prl and sum_bs <= sum_rent:
                sum = sum_bs
            else:
                sum = sum_rent
            if ex_hra_id:
                my_investment = sum
                if my_investment <= ex_hra_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_hra_id.rebate
                self.env['declaration.exemption'].create({
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_hra_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_lunch_id = self.env['saving.master'].sudo().search([('saving_type', '=', 'Lunch Subsidy Allowance'), ('it_rule', '=', 'mus10ale')], limit=1)
            reimbursement_id =  self.env['reimbursement'].sudo().search([('employee_id', '=', rec.employee_id.id),('name', '=', 'lunch'),('from_date', '>', rec.date_range.date_start),('to_date', '<', rec.date_range.date_end),('state', '=', 'approved')])
            sum=0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in reimbursement_id:
                sum+=float(cc.lunch_tds_amt)
            if ex_lunch_id:
                my_investment = sum
                if my_investment <= ex_lunch_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_lunch_id.rebate
                self.env['declaration.exemption'].create({
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_lunch_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_rebate_id = self.env['saving.master'].sudo().search([('saving_type', '=', 'Revised Rebate under Section 87A (2019-20)'), ('it_rule', '=', 'section87a')], limit=1)
            my_investment = 0.00
            my_allowed_rebate = 0.00
            if rec.tax_salary_final <= 50000 and rec.tax_payable >= 12500:
                my_investment = 12500
            elif rec.tax_salary_final <= 50000 and rec.tax_payable <= 12500:
                my_investment = 10000
            elif rec.tax_salary_final >= 50000:
                my_investment = 0
            if ex_rebate_id:
                if my_investment <= ex_rebate_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_rebate_id.rebate
                self.env['declaration.rebate'].create({
                    'rebate_id': rec.id,
                    'it_rule': ex_rebate_id.it_rule,
                    'saving_master': ex_rebate_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_80_c_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Investment in PPF &  Employee’s share of PF contribution'), ('it_rule', '=', '80_c')], limit=1)
            prl_80c_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id),
                 ('slip_id.state', '=', 'done'),
                 ('salary_rule_id.pf_register', '=', True),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            sum = 0
            for sr in prl_80c_id:
                if sr.code == 'CEPF' or sr.code == 'VCPF':
                    sum += sr.amount
            my_investment = 0.00
            my_allowed_rebate = 0.00
            if ex_80_c_id:
                my_investment = sum
                if my_investment <= ex_80_c_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_80_c_id.rebate
                self.env['declaration.slab'].create({
                    'slab_id': rec.id,
                    'it_rule': '80_c',
                    'saving_master': ex_80_c_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            exempt_am = 0.00
            std_am = 0.00
            sum_pt = 0.00
            for std in rec.std_ded_ids:
                std_am += std.allowed_rebate
            for ex in rec.exemption_ids:
                exempt_am += ex.allowed_rebate
            pr_pt_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id), ('slip_id.state', '=', 'done'), ('code', '=', 'PTD'),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            for pt in pr_pt_id:
                sum_pt += pt.amount
            if (rec.tax_salary_final + rec.previous_employer_income - exempt_am) > 0.00:
                rec.income_after_exemption = rec.tax_salary_final + rec.previous_employer_income - exempt_am
            else:
                rec.income_after_exemption = 0.00
            if rec.income_after_exemption - std_am > 0.00:
                rec.income_after_std_ded = rec.income_after_exemption - std_am
            else:
                rec.income_after_std_ded = 0.00
            if rec.income_after_std_ded - sum_pt > 0.00:
                rec.income_after_pro_tax = rec.income_after_std_ded - sum_pt
            else:
                rec.income_after_pro_tax = 0.00
            if (rec.income_after_pro_tax - rec.total_tds_paid - (rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr)) > 0.00:
                rec.taxable_income = rec.income_after_pro_tax - rec.total_tds_paid - (rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr)
            else:
                rec.taxable_income = 0.00
            rec.tax_computed_bool = True
        return True



    def hr_declaration_cron(self):
        search_id = self.env['hr.declaration'].search(
            [('state', 'not in', ['approved', 'rejected', 'verified'])])
        for rec in self:
            sum = 0
            dstart = rec.date_range.date_start - relativedelta(months=1)
            dend = rec.date_range.date_end + relativedelta(months=1)
            proll = self.env['hr.payslip.line'].sudo().search([('slip_id.employee_id', '=', rec.employee_id.id),
                                                               ('slip_id.state', '=', 'done'),
                                                               ('salary_rule_id.taxable_percentage', '>', 0),
                                                               ('slip_id.date_from', '>=', dstart),
                                                               ('slip_id.date_to', '<=', dend)])
            for i in proll:
                sum += i.taxable_amount
            rec.tax_salary_final = sum
            # rec.income_after_rebate = rec.tax_salary_final - rec.net_allowed_rebate
            age = 0
            if rec.employee_id.birthday:
                age = ((datetime.now().date() - rec.employee_id.birthday).days) / 365

            inc_tax_slab = self.env['income.tax.slab'].sudo().search([('salary_from', '<=', rec.tax_salary_final),
                                                                      ('salary_to', '>=', rec.tax_salary_final),
                                                                      ('age_from', '<=', age),
                                                                      ('age_to', '>=', age)], order="create_date desc",
                                                                     limit=1)
            for tax_slab in inc_tax_slab:
                t1 = (tax_slab.tax_rate * (rec.tax_salary_final / 100))
                t2 = (t1 * (1 + tax_slab.surcharge / 100))
                t3 = (t2 * (1 + tax_slab.cess / 100))
                rec.tax_payable = t3
            if rec.tax_payable <= 0.00:
                rec.tax_payable_zero = False
                rec.tax_payable = 0.00
            else:
                rec.tax_payable_zero = True
            rec.std_ded_ids.unlink()
            rec.exemption_ids.unlink()
            rec.rebate_ids.unlink()
            rec.slab_ids.unlink()
            ex_std_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Std. Deduction'), ('it_rule', '=', 'mus10ale')], limit=1)
            my_investment = 0.00
            if ex_std_id:
                my_investment = 0.00
                my_allowed_rebate = 0.00
                if rec.tax_salary_final >= ex_std_id.rebate:
                    my_investment = ex_std_id.rebate
                else:
                    my_investment = rec.tax_salary_final

                if my_investment <= ex_std_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_std_id.rebate
                self.env['declaration.standard'].create({
                    'std_ded_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_std_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_child_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Child Education Allowance & Hostel Expenditure Allowance'),
                 ('it_rule', '=', 'mus10ale')], limit=1)
            child_id = self.env['employee.relative'].sudo().search(
                [('employee_id', '=', rec.employee_id.id)])
            count = 0
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in child_id:
                if cc.relate_type_name == 'Son' or cc.relate_type_name == 'Daughter':
                    count += 1
            if ex_child_id:
                if rec.employee_id.date_of_join and rec.date_range.date_start < rec.employee_id.date_of_join <= rec.date_range.date_end:
                    nm = ((rec.date_range.date_end - rec.employee_id.date_of_join).days) / 30
                    my_investment = count * 100 * nm
                else:
                    my_investment = count * 100 * 12
                if my_investment <= ex_child_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_child_id.rebate

                self.env['declaration.exemption'].create({
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_child_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_hra_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'HRA Exemption'), ('it_rule', '=', 'mus10ale')], limit=1)
            prl_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id), ('slip_id.state', '=', 'done'), ('code', '=', 'HRA'),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            sum_bs = 0.00
            sum_rent = 0.00
            sum_prl = 0.00
            sum = 0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in prl_id:
                sum_prl += cc.amount
            if rec.employee_id.address_home_id.city_id.metro == True:
                sum_bs = ((rec.basic_salary + rec.da_salary) * 50) / 100
            else:
                sum_bs = ((rec.basic_salary + rec.da_salary) * 40) / 100
            sum_rent = rec.rent_paid - ((rec.basic_salary + rec.da_salary) * 10) / 100
            if sum_prl <= sum_bs and sum_prl <= sum_rent:
                sum = sum_prl
            elif sum_bs <= sum_prl and sum_bs <= sum_rent:
                sum = sum_bs
            else:
                sum = sum_rent
            if ex_hra_id:
                my_investment = sum
                if my_investment <= ex_hra_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_hra_id.rebate
                self.env['declaration.exemption'].create({
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_hra_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_lunch_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Lunch Subsidy Allowance'), ('it_rule', '=', 'mus10ale')], limit=1)
            reimbursement_id = self.env['reimbursement'].sudo().search(
                [('employee_id', '=', rec.employee_id.id), ('name', '=', 'lunch'),
                 ('from_date', '>', rec.date_range.date_start), ('to_date', '<', rec.date_range.date_end),
                 ('state', '=', 'approved')])
            sum = 0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in reimbursement_id:
                sum += float(cc.lunch_tds_amt)
            if ex_lunch_id:
                my_investment = sum
                if my_investment <= ex_lunch_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_lunch_id.rebate
                self.env['declaration.exemption'].create({
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_lunch_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_rebate_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Revised Rebate under Section 87A (2019-20)'), ('it_rule', '=', 'section87a')],
                limit=1)
            my_investment = 0.00
            my_allowed_rebate = 0.00
            if rec.tax_salary_final <= 50000 and rec.tax_payable >= 12500:
                my_investment = 12500
            elif rec.tax_salary_final <= 50000 and rec.tax_payable <= 12500:
                my_investment = 10000
            elif rec.tax_salary_final >= 50000:
                my_investment = 0
            if ex_rebate_id:
                if my_investment <= ex_rebate_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_rebate_id.rebate
                self.env['declaration.rebate'].create({
                    'rebate_id': rec.id,
                    'it_rule': ex_rebate_id.it_rule,
                    'saving_master': ex_rebate_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_80_c_id = self.env['saving.master'].sudo().search(
                [('saving_type', '=', 'Investment in PPF &  Employee’s share of PF contribution'),
                 ('it_rule', '=', '80_c')], limit=1)
            prl_80c_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id),
                 ('slip_id.state', '=', 'done'),
                 ('salary_rule_id.pf_register', '=', True),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            sum = 0
            for sr in prl_80c_id:
                if sr.code == 'CEPF' or sr.code == 'VCPF':
                    sum += sr.amount
            my_investment = 0.00
            my_allowed_rebate = 0.00
            if ex_80_c_id:
                my_investment = sum
                if my_investment <= ex_80_c_id.rebate:
                    my_allowed_rebate = my_investment
                else:
                    my_allowed_rebate = ex_80_c_id.rebate
                self.env['declaration.slab'].create({
                    'slab_id': rec.id,
                    'it_rule': '80_c',
                    'saving_master': ex_80_c_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            exempt_am = 0.00
            std_am = 0.00
            sum_pt = 0.00
            for std in rec.std_ded_ids:
                std_am += std.allowed_rebate
            for ex in rec.exemption_ids:
                exempt_am += ex.allowed_rebate
            pr_pt_id = self.env['hr.payslip.line'].sudo().search(
                [('slip_id.employee_id', '=', rec.employee_id.id), ('slip_id.state', '=', 'done'), ('code', '=', 'PTD'),
                 ('slip_id.date_from', '>', rec.date_range.date_start),
                 ('slip_id.date_to', '<', rec.date_range.date_end)])
            for pt in pr_pt_id:
                sum_pt += pt.amount
            if (rec.tax_salary_final + rec.previous_employer_income - exempt_am) > 0.00:
                rec.income_after_exemption = rec.tax_salary_final + rec.previous_employer_income - exempt_am
            else:
                rec.income_after_exemption = 0.00
            if rec.income_after_exemption - std_am > 0.00:
                rec.income_after_std_ded = rec.income_after_exemption - std_am
            else:
                rec.income_after_std_ded = 0.00
            if rec.income_after_std_ded - sum_pt > 0.00:
                rec.income_after_pro_tax = rec.income_after_std_ded - sum_pt
            else:
                rec.income_after_pro_tax = 0.00
            if (rec.income_after_pro_tax - rec.total_tds_paid - (
                    rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr)) > 0.00:
                rec.taxable_income = rec.income_after_pro_tax - rec.total_tds_paid - (
                            rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr)
            else:
                rec.taxable_income = 0.00
            rec.tax_computed_bool = True
        return True

    @api.multi
    def button_payment_tax(self):
        for rec in self:
            rec.tax_payment_ids.unlink()
            edate = rec.date_range.date_end
            date = datetime.now().date().replace(day=1)+ relativedelta(months=1)
            month_cal = ((edate - date).days)/30
            if month_cal > 0:
                amount = (rec.tax_payable)/month_cal
                for i in range(int(month_cal)):
                    self.env['tax.payment'].create({
                        'tax_payment_id': rec.id,
                        'date': date,
                        'amount': amount,
                    })
                    date = date + relativedelta(months=1)


    @api.multi
    def button_verify(self):
        for rec in self:
            if rec.tax_computed_bool == False:
                raise ValidationError(_("Please Compute the tax first"))
            elif not rec.tax_payment_ids:
                raise ValidationError(_("Please fill Tax Payment details"))
            else:
                sum_tax_pay = 0.00
                for data in rec.tax_payment_ids:
                    sum_tax_pay += data.amount
                if not sum_tax_pay == rec.tax_payable:
                    raise ValidationError(_("Sum of Tax Payment Amount should be equal to Tax Payable Amount"))
                else:
                    rec.write({'state': 'verified'})


    @api.model
    def create(self, values):
        res = super(HrDeclaration, self).create(values)
        search_id = self.env['hr.declaration'].search(
            [('employee_id', '=', res.employee_id.id),
             ('state', 'not in', ['draft', 'rejected'])])
        for emp in search_id:
            if res.date_range.date_start <= emp.date_range.date_start or res.date_range.date_start >= emp.date_range.date_end:
                if res.date_range.date_end <= emp.date_range.date_start or res.date_range.date_end >= emp.date_range.date_end:
                    if not (
                            res.date_range.date_start <= emp.date_range.date_start and res.date_range.date_end >= emp.date_range.date_end):
                        index = True
                    else:
                        raise ValidationError(
                            "This declaration is already applied for this duration, please correst the dates 1")
                else:
                    raise ValidationError(
                        "This declaration is already applied for this duration, please correct the dates 2")
            else:
                raise ValidationError(
                    "This declaration is already applied for this duration, please correct the dates 3")
        return res



    @api.multi
    def unlink(self):
        for data in self:
            if data.state not in ('draft', 'rejected'):
                raise UserError(
                    'You cannot delete a Tax which is not in draft or Rejected state')
        return super(HrDeclaration, self).unlink()


class StandardDeclarations(models.Model):
    _name = 'declaration.standard'
    _description = 'Declaration Standard'


    std_ded_id = fields.Many2one('hr.declaration', string='Std Deduction')

    it_rule = fields.Selection([
        ('mus10ale', 'U/S 10 '),
    ], string='IT Rule -Section ')

    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', 'mus10ale')])

    investment = fields.Float(string='investment')
    allowed_rebate = fields.Float(string='Total Std. Deduction')



class ExemptionsDeclarations(models.Model):
    _name = 'declaration.exemption'
    _description = 'declaration.exemption'


    exemption_id = fields.Many2one('hr.declaration', string='Exemption')

    it_rule = fields.Selection([
        ('mus10ale', 'U/S 10 '),
    ], string='IT Rule -Section ')

    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', 'mus10ale')])

    investment = fields.Float(string='Amount Received')
    allowed_rebate = fields.Float(string='Total Exemption')




class RebateDeclarations(models.Model):
    _name = 'declaration.rebate'
    _description = 'declaration.rebate'

    rebate_id = fields.Many2one('hr.declaration', string='Rebate')

    it_rule = fields.Selection([
        ('section87a', 'Section 87A '),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', 'section87a')])
    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate')


class SlabDeclarations(models.Model):
    _name = 'declaration.slab'
    _description = 'declaration.slab'


    slab_id = fields.Many2one('hr.declaration', string='Slab')

    it_rule = fields.Selection([
        ('80_c', '80 C'),
        ('80ccd1', '80CCD (1)'),
        ('80ccd1b', '80CCD (1B)'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type')
    investment = fields.Float(string='Investment')
    document = fields.Binary(string='Document')


class HraDeclarations(models.Model):
    _name = 'declaration.hra'
    _description = 'declaration.hra'

    hra_id = fields.Many2one('hr.declaration', string='HRA')

    it_rule = fields.Selection([
        ('1013a', '10 (13A)'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type')

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')



class MedicalDeclarations(models.Model):
    _name = 'declaration.medical'
    _description = 'declaration.medical'

    med_ins_id = fields.Many2one('hr.declaration', string='Medical')
    saving_master = fields.Many2one('saving.master', string='Saving Type')
    it_rule = fields.Selection([
        ('80d', '80D'),
    ], string='IT Rule -Section ')

    investment = fields.Float(string='Investment')
    document = fields.Binary(string='Document')



class DeductionDeclarations(models.Model):
    _name = 'declaration.deduction'
    _description = 'declaration.deduction'

    deduction_saving_id = fields.Many2one('hr.declaration', string='Deduction Saving')

    it_rule = fields.Selection([
        ('80tta', '80 TTA'),
        ('80ttb', '80 TTB'),
        ('80gg', '80 GG'),
        ('80e', '80E'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type')

    investment = fields.Float(string='Investment')
    document = fields.Binary(string='Document')



class taxhomeDeclarations(models.Model):
    _name = 'declaration.taxhome'
    _description = 'declaration.taxhome'

    tax_home_id = fields.Many2one('hr.declaration', string='TaxHome')

    it_rule = fields.Selection([
        ('80C', '80C'),
        ('24', '24'),
        ('80ee', 'Section 80EE'),
        ('80c', '80c'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type')

    investment = fields.Float(string='Investment')
    document = fields.Binary(string='Document')



class taxeducationDeclarations(models.Model):
    _name = 'declaration.taxeducation'
    _description = 'declaration.taxhome'

    tax_education_id = fields.Many2one('hr.declaration', string='Tax Education')

    it_rule = fields.Selection([
        ('80E', '80 E'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type')

    investment = fields.Float(string='Investment')
    document = fields.Binary(string='Document')


class rgessDeclarations(models.Model):
    _name = 'declaration.rgess'
    _description = 'declaration.rgess'

    rgess_id = fields.Many2one('hr.declaration', string='RGESS')

    it_rule = fields.Selection([
        ('80ccg', '80 CCG'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type')
    investment = fields.Float(string='Investment')
    document = fields.Binary(string='Document')

class dedmedicalDeclarations(models.Model):
    _name = 'declaration.dedmedical'
    _description = 'declaration.dedmedical'

    dedmedical_id = fields.Many2one('hr.declaration', string='DedMedical')

    it_rule = fields.Selection([
        ('80dd', '80 DD'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type')

    investment = fields.Float(string='Investment')
    document = fields.Binary(string='Document')


class dedmedicalselfDeclarations(models.Model):
    _name = 'declaration.dedmedicalself'
    _description = 'declaration.dedmedicalself'

    dedmedical_self_id = fields.Many2one('hr.declaration', string='Ded Medical Self')
    document = fields.Binary(string='Document')

    it_rule = fields.Selection([
        ('80ddb', '80DDB'),
        ('section80g', 'Section 80G'),
        ('80gg', '80 GG'),
        ('us_194_aa', 'u/s 194A'),
    ], string='IT Rule -Section', default='80ddb')
    saving_master = fields.Many2one('saving.master', string='Saving Type')
    investment = fields.Float(string='Investment')




class SavingsMaster(models.Model):
    _name = 'saving.master'
    _description = 'Saving Master'

    it_rule = fields.Selection([
        ('mus10ale', 'U/S 10 '),
        ('section87a', 'Section 87A '),
        ('80_c', '80 C'),
        ('80ccd1', '80CCD (1)'),
        ('80ccd1b', '80CCD (1B)'),
        ('1013a', '10 (13A)'),
        ('80d', '80D'),
        ('80tta', '80 TTA'),
        ('80ttb', '80 TTB'),
        ('80gg', '80 GG'),
        ('80e', '80E'),
        ('80C', '80C'),
        ('24', '24'),
        ('80ee', 'Section 80EE'),
        ('80c', '80c'),
        ('80E', '80 E'),
        ('80ccg', '80 CCG'),
        ('80dd', '80 DD'),
        ('80ddb', '80DDB'),
        ('section80g', 'Section 80G'),
        ('80gg', '80 GG'),
        ('us_194_aa', 'u/s 194A'),
    ], string='IT Rule -Section ')
    saving_type = fields.Char('Saving Type')
    description = fields.Text('Description')
    rebate = fields.Float('Max. Allowed Limit', store=True)


    @api.multi
    @api.depends('saving_type')
    def name_get(self):
        res = []
        name = ''
        for record in self:
            if record.saving_type:
                name = str(record.saving_type)
            else:
                name = 'Savings'
            res.append((record.id, name))
        return res



class RentPaid(models.Model):
    _name = 'rent.paid'
    _description = 'Rent Paid'


    rent_paid_id = fields.Many2one('hr.declaration', string='Rent Paid')
    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')
    amount = fields.Float(string='Amount')
    attchment = fields.Binary(string='Attachment')

    @api.constrains('date_from','date_to')
    def validate_date_f_t(self):
        for rec in self:
            if rec.date_from and rec.rent_paid_id.date_range.date_start and rec.rent_paid_id.date_range.date_end:
                if rec.date_from < rec.rent_paid_id.date_range.date_start or rec.date_from > rec.rent_paid_id.date_range.date_end:
                    raise ValidationError(
                                "From Date must be within Financial year selected")
            if rec.date_to and rec.rent_paid_id.date_range.date_start and rec.rent_paid_id.date_range.date_end:
                if rec.date_to < rec.rent_paid_id.date_range.date_start or rec.date_to > rec.rent_paid_id.date_range.date_end:
                    raise ValidationError(
                                "To Date must be within Financial year selected")
            if rec.date_from and rec.date_to:
                if rec.date_from > rec.date_to:
                    raise ValidationError(
                        "From Date must be less than To Date - Rent Paid")




class TaxPayment(models.Model):
    _name = 'tax.payment'
    _description = 'Tax Payment'

    tax_payment_id = fields.Many2one('hr.declaration', string='Tax Payment')
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    employee_id = fields.Many2one('hr.employee', string='Employee')

