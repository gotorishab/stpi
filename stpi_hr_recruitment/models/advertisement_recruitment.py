from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import datetime


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
    last_date = fields.Date('Last Date',track_visibility='always')
    upload_advertisement = fields.Binary('Upload Advertisement')
    remarks = fields.Text('Remarks (if any)')
    job_position_ids = fields.Many2many('hr.job', string = 'Job Position', domain="[('branch_id', '=', branch_id),('state', '=', 'open')]")
    scpercent = fields.Boolean('Scheduled Castes')
    generalpercent = fields.Boolean('General')
    stpercent = fields.Boolean('Scheduled Tribes')
    obcercent = fields.Boolean('Other Backward Castes')
    ebcpercent = fields.Boolean('Economically Backward Section')
    vhpercent = fields.Boolean('Visually Handicappped')
    hhpercent = fields.Boolean('Hearing Handicapped')
    phpercent = fields.Boolean('Physically Handicapped')


    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Waiting for approval'),
        ('active', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], default='draft', string='Status', track_visibility='always')




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
            lst = []
            if rec.scpercent == True:
                lst.append('Scheduled Castes')
            if rec.generalpercent == True:
                lst.append('General')
            if rec.stpercent == True:
                lst.append('Scheduled Tribes')
            if rec.obcercent == True:
                lst.append('Other Backward Castes')
            if rec.ebcpercent == True:
                lst.append('Economically Backward Section')
            if rec.vhpercent == True:
                lst.append('Visually Handicappped')
            if rec.hhpercent == True:
                lst.append('Hearing Handicapped')
            if rec.phpercent == True:
                lst.append('Physically Handicapped')
            _body = (_(
                (
                    "<ul>Advertisement Created</ul>"
                    "<ul>Allowed Branches: {0} </ul>").format(lst)
            ))
            for jobs in rec.job_position_ids:
                jobs.advertisement_id = rec.id
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



    @api.multi
    def button_complete(self):
        for rec in self:
            _body = (_(
                (
                    "<ul>Advertisement Ended</ul>")
            ))
            for jobs in rec.job_position_ids:
                jobs.message_post(body=_body)
                jobs.set_open()
            rec.write({'state': 'completed'})


    def hr_advertisement_cron(self):
        active_ads = self.env['hr.requisition.application'].search(
            [('state', '=', 'active'), ('last_date', '<=', datetime.now().date())])
        for rec in active_ads:
            rec.sudo().button_complete()



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
