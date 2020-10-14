from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
import re
from datetime import datetime

class RecruitmentJobOpening(models.Model):
    _name = "recruitment.jobop"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Job Opening"

    def default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)


    requested_by = fields.Many2one('hr.employee', string='Requested By', default=default_employee)
    requested_on = fields.Date(string="Requested On", default=fields.Date.today(),track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch')
    job_pos = fields.One2many('job.opening.lines', 'job_opening_id', string='Job Openings')
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('published', 'Published'), ('rejected', 'Rejected')], required=True, string='Status', default='draft', track_visibility='always')


    @api.multi
    def button_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

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
    def button_create_advertisemtnt(self):
        for rec in self:
            create_advertisement = self.env['hr.requisition.application'].create(
                {
                    'state': 'draft',
                    'branch_id': rec.branch_id.id,
                    'start_date': datetime.now().date(),
                }
            )
            sql = self._cr.execute("select job_id,branch_id, count(*) from job_opening_lines" \
                  "group_by job_id,branch" \
                  "where job_opening_id = {0}".format(rec.id))
            print('============sql===================', sql)
            for line in rec.job_pos:
                create_advertisement_line = self.env['advertisement.line'].create(
                    {
                        'allowed_category_id': create_advertisement.id,
                        'job_id': line.job_id.id,
                        'branch_id': line.branch_id.id,
                        'opening': int(line.roster_line_id.sc) + int(line.roster_line_id.general) + int(line.roster_line_id.st),
                        'sc': int(line.roster_line_id.sc),
                        'general': int(line.roster_line_id.general),
                        'st': int(line.roster_line_id.st),
                    }
                )

            rec.write({'state': 'published'})


class RecruitmentJobLines(models.Model):
    _name = "job.opening.lines"


    job_opening_id = fields.Many2one('recruitment.jobop', string='Job Opening')
    job_id = fields.Many2one('hr.job', string='Job Position')
    date = fields.Date(string="Date", default=fields.Date.today(),track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Hiring for Branch')
    roster_line_id = fields.Many2one('recruitment.roster', string='Roster')
    category_id = fields.Many2one('employee.category', string='Category')
    state = fields.Many2one('res.country.state', string='State')
    employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_agency', 'Contractual with Agency'),
                                      ('contractual_with_stpi', 'Contractual with STPI')], string='Employment Type',
                                     track_visibility='always', store=True)

    remarks = fields.Text('Remarks')

