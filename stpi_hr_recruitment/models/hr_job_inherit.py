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
    vacant_post = fields.Integer('Vacant Post', compute='compute_sanctioedpost')

    employee_type = fields.Many2many('employement.type', string='Employment Type')
    # employee_type = fields.Char(string='Employment Type', related='employee_type_name.name')
    state = fields.Selection([
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Not Recruiting')
    ], string='Status', readonly=True, required=True, track_visibility='always', copy=False, default='open',
        help="Set whether the recruitment process is open or closed for this job position.")

    recruitment_type = fields.Selection([
        ('d_recruitment', 'Direct Recruitment(DR)'),
        ('transfer', 'Transfer(Absorption)'),
        ('i_absorption', 'Immediate Absorption'),
        ('deputation', 'Deputation'),
        ('c_appointment', 'Compassionate Appointment'),
        ('promotion', 'Promotion'),
    ], 'Recruitment Type', track_visibility='always')

    technical = fields.Selection([
        ('tech', 'Technical'),
        ('nontech', 'Non Technical'),
    ], 'Technical', track_visibility='always')

    advertisement_id = fields.Many2one('hr.requisition.application', string='Advertisement')
    allowed_degrees = fields.Many2many('hr.recruitment.degree', string='Allowed Degrees')
    pay_level = fields.Many2one('payslip.pay.level', string='Pay Band')
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Type')

    jp = fields.Boolean(string = 'Center - Specific Breakup')
    scpercent = fields.Float('Scheduled Castes %')
    stpercent = fields.Float('Scheduled Tribes %')
    obcercent = fields.Float('Other Backward Castes %')
    ebcpercent = fields.Float('Economically Backward Section %')
    vhpercent = fields.Float('Visually Handicappped %')
    hhpercent = fields.Float('Hearing Handicapped %')
    phpercent = fields.Float('Physically Handicapped %')



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
                'domain': [('job_position_ids', '=', line.id ),
                           ('state', '=', 'active')]
            }


    def _compute_advertisement_count(self):
        for line in self:
            comp_model = self.env['hr.requisition.application'].search([('job_position_ids', '=', line.id),('state', '=', 'active')])
            line.advertisement_count = len(comp_model)


    @api.depends('sanctionedpost')
    def compute_sanctioedpost(self):
        for record in self:
            record.vacant_post = int(record.sanctionedpost) - int(record.no_of_employee)
            if record.vacant_post and record.vacant_post < 0:
                record.vacant_post = 0


    @api.constrains('no_of_recruitment', 'sanctionedpost')
    @api.onchange('no_of_recruitment', 'sanctionedpost')
    def onchange_no_of_recruit(self):
        for record in self:
            if record.sanctionedpost > 0 and int(record.no_of_recruitment) > int(record.vacant_post):
                raise ValidationError(
                    _('Expected new employees count should not be more than vacant position'))



class EmploymentType(models.Model):
    _name='employement.type'
    _description ='Employement Type'

    name = fields.Char('Name')


class HRApplicant(models.Model):
    _inherit='hr.applicant'
    _description ='Applicant'



    @api.constrains('type_id','job_id')
    def check_allowed_branch(self):
        for employee in self:
            if employee.type_id.id not in employee.job_id.allowed_degrees.ids:
                raise ValidationError(_('You are not eligible as you dont have valid degree.'))


