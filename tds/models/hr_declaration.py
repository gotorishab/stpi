from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError

class HrDeclaration(models.Model):
    _name = 'hr.declaration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'HR Declaration'


    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    @api.multi
    @api.depends('slab_ids')
    def _compute_allowed_rebate(self):
        for rec in self:
            total_approved = 0.0
            total_app = 0.00
            for line in rec.slab_ids:
                if line.it_rule == '80_c' or line.it_rule == '80ccd1':
                    total_approved += line.investment
                if line.it_rule == '80ccd1b':
                    total_app += line.investment
            if total_approved <= 150000:
                rec.allowed_rebate_under_80c = total_approved
            else:
                rec.allowed_rebate_under_80c = 150000
            if total_app <= 50000:
                rec.allowed_rebate_under_80b = total_app
            else:
                rec.allowed_rebate_under_80b = 50000
            total_dd = 0.00
            for line in rec.med_ins_ids:
                if line.it_rule == '80d':
                    total_dd += line.investment
            if total_dd <= 150000:
                rec.allowed_rebate_under_80d = total_dd
            else:
                rec.allowed_rebate_under_80d = 150000
            total_dsa = 0.00
            for line in rec.deduction_saving_ids:
                if line.it_rule:
                    total_dsa += line.investment
            if total_dsa <= 150000:
                rec.allowed_rebate_under_80dsa = total_dsa
            else:
                rec.allowed_rebate_under_80dsa = 150000
            total_tbhl = 0.00
            total_ee = 0.00
            total_24 = 0.00
            for line in rec.tax_home_ids:
                if line.it_rule == '80ee':
                    total_ee += line.investment
                elif line.it_rule == '24':
                    total_24 += line.investment
                else:
                    total_tbhl += line.investment
            if total_ee <= 150000:
                rec.allowed_rebate_under_80ee = total_ee
            else:
                rec.allowed_rebate_under_80ee = 150000
            if total_24 <= 50000:
                rec.allowed_rebate_under_24 = total_24
            else:
                rec.allowed_rebate_under_24 = 50000
            if total_tbhl <= 50000:
                rec.allowed_rebate_under_tbhl = total_tbhl
            else:
                rec.allowed_rebate_under_tbhl = 50000
            total_tei = 0.00
            for line in rec.tax_education_ids:
                if line.it_rule:
                    total_tei += line.investment
            if total_tei <= 150000:
                rec.allowed_rebate_under_80e = total_tei
            else:
                rec.allowed_rebate_under_80e = 150000
            total_80ccg = 0.00
            for line in rec.rgess_ids:
                if line.it_rule:
                    total_80ccg += line.investment
            if total_80ccg <= 150000:
                rec.allowed_rebate_under_80ccg = total_80ccg
            else:
                rec.allowed_rebate_under_80ccg = 150000
            total_80dd = 0.00
            for line in rec.dedmedical_ids:
                if line.it_rule:
                    total_80dd += line.investment
            if total_80dd <= 150000:
                rec.allowed_rebate_under_80cdd = total_80dd
            else:
                rec.allowed_rebate_under_80cdd = 150000
            total_80mesdr = 0.00
            for line in rec.dedmedical_self_ids:
                if line.it_rule:
                    total_80mesdr += line.investment
            if total_80mesdr <= 150000:
                rec.allowed_rebate_under_80mesdr = total_80mesdr
            else:
                rec.allowed_rebate_under_80mesdr = 150000


    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee, track_visibility='always')


    job_id = fields.Many2one('hr.job', string="Functional Designation", store=True, track_visibility='always')
    branch_id = fields.Many2one('res.branch', string="Branch", store=True, track_visibility='always')
    department_id = fields.Many2one('hr.department', string="Department", store=True, track_visibility='always')


    date_range = fields.Many2one('date.range','Date Range', track_visibility='always')
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True, track_visibility='always')
    tax_salary_final = fields.Float(string='Taxable Salary', store=True, track_visibility='always')
    exemption_ids = fields.One2many('declaration.exemption', 'exemption_id', string='Exemption Ids')
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
    net_allowed_rebate = fields.Float('Net Allowed Rebate', compute='compute_net_allowed_rebate')
    income_after_rebate = fields.Float('Income after Rebate')
    tax_payable = fields.Float('Tax Payable(%)')
    tax_payable_zero = fields.Boolean('Tax Payable(%) greater than equal to zero')
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


    @api.depends('exemption_ids','rebate_ids','allowed_rebate_under_80c','allowed_rebate_under_80b','allowed_rebate_under_80d','allowed_rebate_under_80dsa','allowed_rebate_under_80e','allowed_rebate_under_80ccg','allowed_rebate_under_tbhl','allowed_rebate_under_80ee','allowed_rebate_under_24','allowed_rebate_under_80cdd', 'allowed_rebate_under_80mesdr')
    def compute_net_allowed_rebate(self):
        for rec in self:
            sum=0.00
            sum1 = 0.00
            for de in rec.exemption_ids:
                sum+=de.allowed_rebate
            for de in rec.rebate_ids:
                sum+=de.allowed_rebate
            sum1 = rec.allowed_rebate_under_80c + rec.allowed_rebate_under_80b + rec.allowed_rebate_under_80d + rec.allowed_rebate_under_80dsa + rec.allowed_rebate_under_80e + rec.allowed_rebate_under_80ccg + rec.allowed_rebate_under_tbhl + rec.allowed_rebate_under_80ee + rec.allowed_rebate_under_24 + rec.allowed_rebate_under_80cdd + rec.allowed_rebate_under_80mesdr
            rec.net_allowed_rebate = sum + sum1


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
            proll =  self.env['hr.payslip.line'].search([('slip_id.employee_id', '=', rec.employee_id.id),
                                                         ('slip_id.state', '=', 'done'),
                                                         ('salary_rule_id.taxable_percentage', '>', 0),
                                                         ('slip_id.date_from', '>', rec.date_range.date_start),
                                                         ('slip_id.date_to', '<', rec.date_range.date_end)])
            for i in proll:
                sum += i.taxable_amount
            rec.tax_salary_final = sum
            rec.income_after_rebate = rec.tax_salary_final - rec.net_allowed_rebate
            age = 0
            if rec.employee_id.birthday:
                age = ((datetime.now().date() - rec.employee_id.birthday).days) / 365

            inc_tax_slab =  self.env['income.tax.slab'].search([('salary_from', '<=', rec.tax_salary_final),
                                                                ('salary_to', '>=', rec.tax_salary_final),
                                                                ('age_from', '<=', age),
                                                                ('age_to', '>=', age)],order ="create_date desc",
                                                               limit=1)
            for tax_slab in inc_tax_slab:
                t1 = ((tax_slab.tax_rate * rec.tax_salary_final)/100)
                t2 = (t1 * tax_slab.surcharge)/100
                t3 = (t2 * tax_slab.cess)/100
                t4 = t2 + t3
                rec.tax_payable = t4
            else:
                rec.tax_payable = 0.00
            if rec.tax_payable <= 0.00:
                rec.tax_payable_zero = False
            else:
                rec.tax_payable_zero = True
            rec.exemption_ids.unlink()
            rec.rebate_ids.unlink()
            ex_std_id = self.env['saving.master'].search(
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
                self.env['declaration.exemption'].create({
                    'exemption_id': rec.id,
                    'it_rule': 'mus10ale',
                    'saving_master': ex_std_id.id,
                    'investment': my_investment,
                    'allowed_rebate': my_allowed_rebate,
                })
            ex_child_id = self.env['saving.master'].search(
                [('saving_type', '=', 'Child Education Allowance & Hostel Expenditure Allowance'), ('it_rule', '=', 'mus10ale')], limit=1)
            child_id = self.env['employee.relative'].search(
                [('employee_id', '=', rec.employee_id.id)])
            count = 0
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in child_id:
                if cc.relate_type_name == 'Son' or cc.relate_type_name == 'Daughter':
                    count+=1
            if ex_child_id:
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
            ex_hra_id = self.env['saving.master'].search([('saving_type', '=', 'HRA Exemption'), ('it_rule', '=', 'mus10ale')], limit=1)
            prl_id =  self.env['hr.payslip.line'].search([('slip_id.employee_id', '=', rec.employee_id.id),('slip_id.state', '=', 'done'),('code', '=', 'HRA'),('slip_id.date_from', '>', rec.date_range.date_start),('slip_id.date_to', '<', rec.date_range.date_end)])
            sum=0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in prl_id:
                sum+=cc.taxable_amount
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
            ex_lunch_id = self.env['saving.master'].search([('saving_type', '=', 'Lunch Subsidy Allowance'), ('it_rule', '=', 'mus10ale')], limit=1)
            reimbursement_id =  self.env['reimbursement'].search([('employee_id', '=', rec.employee_id.id),('name', '=', 'lunch'),('from_date', '>', rec.date_range.date_start),('to_date', '<', rec.date_range.date_end)])
            sum=0.00
            my_investment = 0.00
            my_allowed_rebate = 0.00
            for cc in reimbursement_id:
                sum+=float(cc.net_amount)
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
                    'allowed_ rebate': my_allowed_rebate,
                })
            ex_rebate_id = self.env['saving.master'].search([('saving_type', '=', 'Revised Rebate under Section 87A (2019-20)'), ('it_rule', '=', 'section87a')], limit=1)
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
            rec.tax_computed_bool = True
        return True


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


    @api.multi
    def unlink(self):
        for data in self:
            if data.state not in ('draft', 'rejected'):
                raise UserError(
                    'You cannot delete a Tax which is not in draft or Rejected state')
        return super(HrDeclaration, self).unlink()

class ExemptionsDeclarations(models.Model):
    _name = 'declaration.exemption'
    _description = 'declaration.exemption'


    exemption_id = fields.Many2one('hr.declaration', string='Exemption')

    it_rule = fields.Selection([
        ('mus10ale', 'U/S 10 '),
    ], string='IT Rule -Section ')

    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', 'mus10ale')])

    investment = fields.Float(string='investment')
    allowed_rebate = fields.Float(string='Allowed Rebate')




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
    saving_master = fields.Many2one('saving.master', string='Saving Type',
                                    domain=[('it_rule', 'in', ('80_c', '80ccd1', '80ccd1b'))])
    it_rule = fields.Selection([
        ('80_c', '80 C'),
        ('80ccd1', '80CCD (1)'),
        ('80ccd1b', '80CCD (1B)'),
    ], string='IT Rule -Section ')

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float('Allowed Rebate')
    document = fields.Binary(string='Document')


class HraDeclarations(models.Model):
    _name = 'declaration.hra'
    _description = 'declaration.hra'

    hra_id = fields.Many2one('hr.declaration', string='HRA')

    it_rule = fields.Selection([
        ('1013a', '10 (13A)'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', '1013a')])

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment



class MedicalDeclarations(models.Model):
    _name = 'declaration.medical'
    _description = 'declaration.medical'

    med_ins_id = fields.Many2one('hr.declaration', string='Medical')
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', '80d')])
    it_rule = fields.Selection([
        ('80d', '80D'),
    ], string='IT Rule -Section ')

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment



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
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', 'in', ('80tta', '80ttb', '80gg', '80e'))])

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment



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
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', 'in', ('80C', '24', '80ee', '80c'))])

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment



class taxeducationDeclarations(models.Model):
    _name = 'declaration.taxeducation'
    _description = 'declaration.taxhome'

    tax_education_id = fields.Many2one('hr.declaration', string='Tax Education')

    it_rule = fields.Selection([
        ('80E', '80 E'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', '80E')])

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment



class rgessDeclarations(models.Model):
    _name = 'declaration.rgess'
    _description = 'declaration.rgess'

    rgess_id = fields.Many2one('hr.declaration', string='RGESS')

    it_rule = fields.Selection([
        ('80ccg', '80 CCG'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', '80ccg')])

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment

class dedmedicalDeclarations(models.Model):
    _name = 'declaration.dedmedical'
    _description = 'declaration.dedmedical'

    dedmedical_id = fields.Many2one('hr.declaration', string='DedMedical')

    it_rule = fields.Selection([
        ('80dd', '80 DD'),
    ], string='IT Rule -Section ')
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', '=', '80dd')])

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')
    document = fields.Binary(string='Document')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment


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
    saving_master = fields.Many2one('saving.master', string='Saving Type', domain=[('it_rule', 'in', ('80ddb', 'section80g', '80gg','us_194_aa'))])

    investment = fields.Float(string='Investment')
    allowed_rebate = fields.Float(string='Allowed Rebate', compute='compute_allowed_rebate')

    @api.depends('allowed_rebate')
    def compute_allowed_rebate(self):
        for rec in self:
            if rec.saving_master.rebate and rec.investment:
                rec.allowed_rebate = rec.saving_master.rebate - rec.investment



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
    rebate = fields.Float('Rebate', store=True)


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



class TaxPayment(models.Model):
    _name = 'tax.payment'
    _description = 'Tax Payment'

    tax_payment_id = fields.Many2one('hr.declaration', string='Tax Payment')
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    employee_id = fields.Many2one('hr.employee', string='Employee')

