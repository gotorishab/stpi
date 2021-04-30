from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
import re
from datetime import datetime

class RecruitmentRoster(models.Model):
    _name = "recruitment.roster"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Recruitment Roster"
    _rec_name = 'number'

    # @api.onchange('job_id')
    # def get_roster_line_item(self):
    #     return {'domain': {'roster_line_item': [('job_id', '=', self.job_id.id), ('employee_id', '=', False)]}}


    # sequence_number = fields.Integer('Sequence Number')
    number = fields.Char('Number')

    name = fields.Integer(string="Sequence Number",track_visibility='always')
    roster_point_number = fields.Many2one('recruitment.roster', string='Roster Point Number')
    category_id = fields.Many2many('employee.category', string='Reserved For')
    state = fields.Many2one('res.country.state', string='State')
    emp_code = fields.Char('Emp Code')
    employee_id = fields.Many2one('hr.employee', string='Name of the Person')
    Name_of_person = fields.Char('Name of the Person')
    Hired_category = fields.Many2one('employee.category', string='Utilised By')
    date_of_apointment = fields.Date('Date of Appointment')
    current_status = fields.Selection([('Resigned', 'Resigned'),
                                      ('Working', 'Working'),
                                      ('Vacant', 'Vacant'),
                                       ], string='Current Status')
    current_status_date = fields.Date(string='Current Status Date')
    job_id = fields.Many2one('hr.job', string='Current Designation')
    remarks = fields.Text('Remarks')



    @api.model
    def create(self, vals):
        res = super(RecruitmentRoster, self).create(vals)
        res.number = str(res.name) + ' (' + str(res.job_id.name) + ')' + ' (' + str(res.category_id.name) + ')' + ' (' + str(res.state.name) + ')'
        print('============================', res.number)
        return res


class EmployeeRoster(models.Model):
    _inherit = "hr.employee"

    roster_line_item = fields.Many2one('recruitment.roster', string="Roster line")


    @api.constrains('roster_line_item')
    def putinto_roster_line_item(self):
        for rec in self:
            if rec.roster_line_item:
                rec.roster_line_item.employee_id = rec.id
                rec.roster_line_item.Hired_category = rec.category.id
                rec.roster_line_item.emp_code = rec.identify_id
                rec.roster_line_item.Name_of_person = rec.name
                rec.roster_line_item.date_of_apointment = rec.date_of_join