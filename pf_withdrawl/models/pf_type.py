from odoo import models, fields, api,_

class PfType(models.Model):

    _name="pf.type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "PF Type"


    name = fields.Char(string="PF Type",track_visibility='always')
    purpose = fields.Text(string="Purpose",track_visibility='always')
    months = fields.Integer(string='Months')
    voluntarily_contri = fields.Boolean('Volunteerly')
    employee_contri = fields.Boolean('Employee')
    employer_contri = fields.Boolean('Employer')
    min_years = fields.Integer(string='Minimum age(Years)')
    attachment_document = fields.Text(string="Attachment Document",track_visibility='always')