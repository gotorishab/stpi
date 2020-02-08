from odoo import api, fields, models, tools, _


class TDS(models.Model):
    _name = "tds"
    _description = "TDS"

    employee_id = fields.Many2one('hr.employee', string='Employee')
    date_range = fields.Many2one('date.range','Date range')


class IncomeTaxSlab(models.Model):
    _name = "income.tax.slab"
    _description = "Income Tax Slab"

    salary_from = fields.Float(string='Salary From')
    salary_to = fields.Float(string='Salary To')
    tax_rate = fields.Float(string='Tax Rate(%)')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('both', 'Both'),
    ], string='Gender')
    age_from = fields.Integer(string='Age From')
    age_to = fields.Integer(string='Age To')
    surcharge_ids = fields.Many2many('tax.surcharge', string='Surcharge')
    surcharge = fields.Float(string='Surcharge')
    surcharge_extra = fields.Float(string='Surcharge Extra')


class ReimbursementTution(models.Model):
    _name = "tax.surcharge"
    _description = "Income Tax Surcharge"

    name = fields.Char(string='Name')


class SalaryRules_inh(models.Model):
    _inherit = "hr.salary.rule"
    _description = "Salary Rule"

    taxable_percentage = fields.Float(string='Taxable Percentage')
    pf_register = fields.Boolean(string='Register PF?')