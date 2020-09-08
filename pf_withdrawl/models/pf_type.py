from odoo import models, fields, api,_

class PfType(models.Model):

    _name="pf.type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "PF Withdrawal Type"


    name = fields.Char(string="PF Withdrawal Type",track_visibility='always')
    purpose = fields.Text(string="Purpose",track_visibility='always')
    months = fields.Integer(string='Month (Basic+DA)')
    voluntarily_contri = fields.Boolean('Volunteerly')
    cepf_vcpf = fields.Boolean('CEPF + VCPF')
    cpf = fields.Boolean('CPF')
    employee_contri = fields.Boolean('Employee')
    employer_contri = fields.Boolean('Employer')
    min_years = fields.Integer(string='Minimum age(Years)')
    attachment_document = fields.Text(string="Attachment Document",track_visibility='always')