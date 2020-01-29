from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class HRRequisitionInherit(models.Model):
    _inherit='hr.requisition'
    _description ='HR Requisition'

#     department_id = fields.Many2one('hr.department', string="Department",
#                                     related="job_position.department_id",
#                                     help='Department of the employee')
#
#     @api.constrains('no_of_employee')
#     @api.onchange('no_of_employee')
#     def onchange_no_of_employee(self):
#         for record in self:
#             if int(record.no_of_employee) < 0:
#                 raise ValidationError(
#                     _('The number of Position should be greater than 0'))
#
#     @api.constrains('deadline_date')
#     @api.onchange('deadline_date')
#     def onchange_deadline_datee(self):
#         for record in self:
#             if record.deadline_date and record.date and record.deadline_date < record.date:
#                 raise ValidationError(
#                     _('Deadline date should be greater than or equal to date, but should not be less than date'))
#
#
# class ReasonCodeInherit(models.Model):
#     _inherit='hr.reason.code'
#     _description ='HR Reason Code'
#
#     description = fields.Text('Description')


class HrApplicationSd(models.Model):
    _name = 'hr.requisition.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hr Requisition Application'

    name = fields.Char('Advertisement Number')
    branch_id = fields.Many2one('res.branch', string='Branch')
    contact = fields.Char('Contact')
    advertisement_number = fields.Char('Advertisement No.')
    advertisement_dated = fields.Date('Advertisement Dated')
    start_date = fields.Date('Start Date')
    last_date = fields.Date('Last Date')
    upload_advertisement = fields.Binary('Upload Advertisement')
    remarks = fields.Text('Remarks (if any)')
    job_position_ids = fields.Many2many('hr.job', string = 'Job Position', domain="[('branch_id', '=', branch_id),('state', '=', 'open')]")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Waiting for approval'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], default='draft')



    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.multi
    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'to_approve'})

    @api.multi
    def button_active(self):
        for rec in self:
            _body = (_(
                (
                    "<ul>Advertisement Created</ul>")
            ))
            for jobs in rec.job_position_ids:
                jobs.message_post(body=_body)
                jobs.set_recruit()
            rec.write({'state': 'active'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_update(self):
        for rec in self:
            pass

    def hr_advertisement_cron(self):
        for line in self:
            todays_date = datetime.now().date()
            if line.last_date == todays_date:
                line.state = 'completed'



    @api.model
    def create(self, vals):
        res =super(HrApplicationSd, self).create(vals)
        sequence = ''
        seq = self.env['ir.sequence'].next_by_code('hr.requisition.application')
        sequence = 'Adv. ' + str(seq)
        # res.adv_sequence = sequence
        res.name = sequence
        return res

    @api.multi
    @api.depends('name')
    def name_get(self):
        res = []
        for record in self:
            if record.name:
                name = record.name
            else:
                name = 'Advertisement'
            res.append((record.id, name))
        return res


    @api.onchange('job_position_ids')
    @api.constrains('job_position_ids')
    def check_existing_job(self):
        for line in self:
            comp_model = self.env['hr.requisition.application'].search([('state', '=', 'active'),('job_position_ids', '=', line.job_position_ids.ids)])
            if comp_model:
                raise ValidationError(
                    _('Already advertised'))



    @api.constrains('start_date','last_date')
    @api.onchange('start_date','last_date')
    def onchange_date_sl(self):
        for record in self:
            if record.start_date and record.last_date and record.start_date > record.last_date:
                raise ValidationError(
                    _(
                        'Advertisement start date must be less than last date'))
