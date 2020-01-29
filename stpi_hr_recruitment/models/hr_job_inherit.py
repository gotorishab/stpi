from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class HRJobInherit(models.Model):
    _inherit='hr.job'
    _description ='HR Job'

    branch_id = fields.Many2one('res.branch', 'Branch')
    no_of_recruitment = fields.Integer(string='Expected New Employees', copy=False,
                                       help='Number of new employees you expect to recruit.', default=0)
    sanctionedpost = fields.Integer('Sactioned Posts')
    advertisement_count = fields.Integer('Advertisement count', compute='_compute_advertisement_count')
    vacant_post = fields.Integer('Vacant Post')
    employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_agency', 'Contractual with Agency'),
                                      ('contractual_with_stpi', 'Contractual with STPI')], string='Employment Type',
                                     track_visibility='always')

    state = fields.Selection(selection_add=[('budget', 'Budget')], default='open')


    recruitment_type = fields.Selection([
        ('d_recruitment', 'Direct Recruitment(DR)'),
        ('transfer', 'Transfer(Absorption)'),
        ('i_absorption', 'Immediate Absorption'),
        ('deputation', 'Deputation'),
        ('c_appointment', 'Compassionate Appointment'),
        ('promotion', 'Promotion'),
    ], 'Recruitment Type', track_visibility='always')


    def see_all_advertisements(self):
        for line in self:
            # comp_model = self.env['hr.requisition.application'].search([])
            return {
                'name': 'Hr Requisition Application',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'hr.requisition.application',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'domain': [('job_position_ids', '=', line.id )]
            }


    def _compute_advertisement_count(self):
        for line in self:
            comp_model = self.env['hr.requisition.application'].search([('job_position_ids', '=', line.id)])
            line.advertisement_count = len(comp_model)


    # @api.depends('sanctionedpost')
    # def compute_sanctioedpost(self):
    #     for record in self:
    #         employe = self.env['hr.employee'].search([('employee_type', '=', 'regular')])
    #         count = 0
    #         for emp in employe:
    #             count+=1
    #         record.vacant_post = int(record.sanctionedpost) - int(count)
    #         if record.vacant_post and record.vacant_post < 0:
    #             record.vacant_post = 0

    @api.constrains('no_of_recruitment')
    @api.onchange('no_of_recruitment')
    def onchange_no_of_recruit(self):
        for record in self:
            if record.employee_type == 'regular' and int(record.no_of_recruitment) > int(record.vacant_post):
                record.no_of_recruitment = 0
                raise ValidationError(
                    _('Expected new employees count should not be more than vacant position'))
