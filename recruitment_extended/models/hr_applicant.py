from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class Applicant(models.Model):
    _inherit = "hr.applicant"

    date_of_birth = fields.Date('Date Of Birth')
    place_of_birth = fields.Char('Place Of Birth')