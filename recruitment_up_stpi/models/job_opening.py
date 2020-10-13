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

    #
    # @api.multi
    # def button_create_advertisemtnt(self):
    #     for rec in self:
    #         create_advertisement = self.env['hr.requisition.application'].create(
    #             {
    #                 'state': 'draft',
    #                 'branch_id': rec.branch_id.id,
    #                 'start_date': datetime.now().date(),
    #             }
    #         )
    #         rec.write({'state': 'published'})


    @api.multi
    def button_create_advertisemtnt(self):
        for rec in self:
            for line in rec.job_pos:

            # detail_of_journey = []
            create_advertisement = self.env['hr.requisition.application'].create(
                {
                    'state': 'draft',
                    'branch_id': rec.branch_id.id,
                    'start_date': datetime.now().date(),
                    # 'advertisement_line_ids':
                    #     ((0, 0, {
                    #     'job_ids': rec.id,
                    #     'branch_id': i.departure_date,
                    #     'department_id': i.departure_time,
                    #     'opening': i.arrival_date,
                    #     'sc': i.arrival_time,
                    #     'general': i.from_l.id,
                    #     'st': i.to_l.id,
                    #     }))
                }
            )
            rec.write({'state': 'published'})
            print('==================================================', create_advertisement.id)


class RecruitmentJobLines(models.Model):
    _name = "job.opening.lines"


    job_opening_id = fields.Many2one('recruitment.jobop', string='Job Opening')
    job_id = fields.Many2one('hr.job', string='Job Position')
    date = fields.Date(string="Date", default=fields.Date.today(),track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch')
    roster_line_id = fields.Many2one('recruitment.roster', string='Roster')
