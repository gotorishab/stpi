from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


class ResumeLine(models.Model):
    _inherit = 'hr.employee'

