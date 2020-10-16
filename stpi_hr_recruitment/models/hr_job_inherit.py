from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import  datetime
from dateutil.relativedelta import relativedelta


class HRJobInherit(models.Model):
    _inherit='hr.job'
    _description ='HR Job'

    branch_id = fields.Many2one('res.branch', 'Branch')
    no_of_recruitment = fields.Integer(string='Expected New Employees', copy=False,
                                       help='Number of new employees you expect to recruit.', default=0)
    sanctionedpost = fields.Integer('Sactioned Posts')
    advertisement_count = fields.Integer('Advertisement count', compute='_compute_advertisement_count')
    vacant_post = fields.Integer('Vacant Post', compute='compute_sanctioedpost')

    employee_type = fields.Many2many('employement.type', string='Employment Type', track_visibility='always')
    recruitment_type = fields.Many2many('recruitment.type', string='Recruitment Type', track_visibility='always')
    # employee_type = fields.Char(string='Employment Type', related='employee_type_name.name')
    state = fields.Selection([
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Not Recruiting')
    ], string='Status', readonly=True, required=True, track_visibility='always', copy=False, default='open',
        help="Set whether the recruitment process is open or closed for this job position.")
    #
    # recruitment_type = fields.Selection([
    #     ('d_recruitment', 'Direct Recruitment(DR)'),
    #     ('transfer', 'Transfer(Absorption)'),
    #     ('i_absorption', 'Immediate Absorption'),
    #     ('deputation', 'Deputation'),
    #     ('c_appointment', 'Compassionate Appointment'),
    #     ('promotion', 'Promotion'),
    # ], 'Recruitment Type', track_visibility='always')

    technical = fields.Selection([
        ('tech', 'Technical'),
        ('nontech', 'Non Technical'),
    ], 'Technical', track_visibility='always')

    advertisement_id = fields.Many2one('hr.requisition.application', string='Advertisement')
    allowed_degrees = fields.Many2many('hr.recruitment.degree', string='Allowed Degrees')

    vacant_p_z = fields.Boolean(string='Is vacant post less than zero', compute="compute_sanctioedpost", store=1)

    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level')
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Type')

    jp = fields.Boolean(string = 'Center - Specific Breakup')
    scpercent = fields.Float('Scheduled Castes %')
    stpercent = fields.Float('Scheduled Tribes %')
    obcercent = fields.Float('Other Backward Castes %')
    ebcpercent = fields.Float('Economically Backward Section %')
    vhpercent = fields.Float('Visually Handicappped %')
    hhpercent = fields.Float('Hearing Handicapped %')
    phpercent = fields.Float('Physically Handicapped %')



    @api.depends('birthday')
    def _check_next_month(self):
        for rec in self:
            month = (datetime.datetime.now().replace(day=1)+ relativedelta(months=1)).strftime("%m")
            if rec.birthday:
                bday_month = rec.birthday.strftime("%m")
                if month == bday_month:
                    rec.is_next_month = True
                else:
                    rec.is_next_month = False


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
            if record.vacant_post and record.vacant_post > 0:
                record.vacant_p_z = False


    @api.constrains('no_of_recruitment', 'sanctionedpost')
    @api.onchange('no_of_recruitment', 'sanctionedpost')
    def onchange_no_of_recruit(self):
        for record in self:
            if record.sanctionedpost > 0 and int(record.no_of_recruitment) > int(record.vacant_post):
                raise ValidationError(
                    _('Expected new employees count should not be more than vacant position'))



class EmploymentType(models.Model):
    _name = 'employement.type'
    _description ='Employement Type'

    name = fields.Char('Name')

class RecruitmentType(models.Model):
    _name = 'recruitment.type'
    _description ='Recruitment Type'

    name = fields.Char('Name')


class HRApplicant(models.Model):
    _inherit='hr.applicant'
    _description ='Applicant'

    advertisement_id = fields.Many2one('hr.requisition.application', string='Advertisement')
    advertisement_id_related = fields.Many2one('hr.requisition.application', string='Advertisement', related='advertisement_id')
    advertisement_line_id = fields.Many2one('advertisement.line', string='Advertisement Line')

    @api.onchange('advertisement_line_id')
    @api.constrains('advertisement_line_id')
    def get_job_advertonch(self):
        for rec in self:
            rec.job_id = rec.advertisement_line_id.job_id
            rec.struct_id = rec.advertisement_line_id.job_id.struct_id
            rec.employee_type = rec.advertisement_line_id.job_id.employee_type
            rec.branch_id = rec.advertisement_line_id.job_id.branch_id