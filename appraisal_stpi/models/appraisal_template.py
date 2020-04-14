from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta

class AppraisalTemplate(models.Model):
    _name = 'appraisal.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appraisal Template'

    name = fields.Char('Template Name')
    kpi_kpa_ids = fields.One2many('appraisal.template.o2m', 'kpi_kpa_id')

    @api.constrains('kpi_kpa_ids','name')
    def validate_weightage(self):
        for rec in self:
            sum = 0.00
            for line in rec.kpi_kpa_ids:
                sum += line.weigtage
            if int(sum) != 100:
                raise ValidationError(
                    "Weightage must be equal to 100")



class AppraisalTemplateOtM(models.Model):
    _name = 'appraisal.template.o2m'
    _description = 'Appraisal Template O2m'

    kpi_kpa_id = fields.Many2one('appraisal.template', string='ID')
    kpi = fields.Char('KPI')
    kra = fields.Char('KRA')
    weigtage = fields.Float('Weightage')
