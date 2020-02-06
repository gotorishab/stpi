from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class Reimbursement(models.Model):

    _name = "reimbursement.attendence"
    _description = "Reimbursement Attendence"


    employee_id = fields.Many2one('hr.employee', string='Employee')
    year = fields.Char(size=4, readonly=True)
    month = fields.Selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
                              ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
                              ('10', 'October'), ('11', 'November'), ('12', 'December')])
    present_days = fields.Float('Present Days')
    no_of_days = fields.Float('Maximum number of Days')
