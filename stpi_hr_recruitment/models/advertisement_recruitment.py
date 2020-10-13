from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import datetime


class HrApplicationSd(models.Model):
    _name = 'hr.requisition.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hr Requisition Application'


    name = fields.Char('Sequence')
    branch_id = fields.Many2one('res.branch', string='Branch')
    contact = fields.Char('Contact')
    advertisement_number = fields.Char('Advertisement No.')
    advertisement_dated = fields.Date('Advertisement Dated')
    start_date = fields.Date('Start Date')
    last_date = fields.Date('Last Date',track_visibility='always')
    upload_advertisement = fields.Binary('Upload Advertisement')
    remarks = fields.Text('Remarks (if any)')
    job_position_ids = fields.Many2many('hr.job', string = 'Job Position')
    allowed_categories_ids = fields.One2many('allowed.categories','allowed_category_id', string='Allowed Categories')
    advertisement_line_ids = fields.One2many('advertisement.line','allowed_category_id', string='Advertisement Lines')

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
            # rec.allowed_categories_ids.unlink()
            # allowed_categories_ids = []
            # for jobs in rec.job_position_ids:
            #     allowed_categories_ids.append((0, 0, {
            #             'job_id': jobs.id,
            #             'vacant_post': jobs.vacant_post,
            #             'allowed_category_id': rec.id,
            #         }))
            # rec.allowed_categories_ids = allowed_categories_ids
            rec.write({'state': 'to_approve'})

    @api.multi
    def button_active(self):
        for rec in self:
            for allowed in rec.advertisement_line_ids:
                _body = (_(
                    (
                        "<ul>Advertisement Created</ul>"
                        "<ul>Opening: {0} </ul>"
                        "<ul>Scheduled Caste: {1} </ul>"
                        "<ul>Scheduled Tribes: {2} </ul>"
                        "<ul>General: {3} </ul>"
                        "<ul>Branch: {4} </ul>"
                    ).format(allowed.opening, allowed.sc, allowed.st, allowed.general, allowed.branch_id)
                ))
                # for jobs in allowed.job_ids:
                allowed.job_id.advertisement_id = rec.id
                allowed.job_id.message_post(body=_body)
                allowed.job_id.set_recruit()
            rec.write({'state': 'active'})
    #
    #
    # @api.multi
    # def button_active(self):
    #     for rec in self:
    #         sum=0
    #         sum_vac = 0
    #         lst = []
    #         for allowed in rec.allowed_categories_ids:
    #             sum_vac += (allowed.vacant_post)
    #             sum += (allowed.scpercent + allowed.generalpercent + allowed.stpercent + allowed.obcercent + allowed.ebcpercent + allowed.vhpercent + allowed.hhpercent + allowed.phpercent)
    #             _body = (_(
    #                 (
    #                     "<ul>Advertisement Created</ul>"
    #                     "<ul>Allowed Categories: </ul>"
    #                     "<ul>Scheduled Castes: {0} </ul>"
    #                     "<ul>Allowed Categories: {1} </ul>"
    #                     "<ul>Scheduled Tribes: {2} </ul>"
    #                     "<ul>Other Backward Castes: {3} </ul>"
    #                     "<ul>Economically Backward Section: {4} </ul>"
    #                     "<ul>Visually Handicappped: {5} </ul>"
    #                     "<ul>Hearing Handicapped: {6} </ul>"
    #                     "<ul>Physically Handicapped: {7} </ul>"
    #                 ).format(allowed.scpercent, allowed.generalpercent, allowed.stpercent, allowed.obcercent,
    #                          allowed.ebcpercent, allowed.vhpercent, allowed.hhpercent, allowed.phpercent)
    #             ))
    #         if sum_vac > 0 and sum <= 0:
    #             raise ValidationError(
    #                     _(
    #                         'Allowed Categories must be greater than 0'))
    #         else:
    #             for jobs in rec.job_position_ids:
    #                 jobs.advertisement_id = rec.id
    #                 jobs.message_post(body=_body)
    #                 jobs.set_recruit()
    #         rec.write({'state': 'active'})

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

    @api.multi
    def button_complete(self):
        for rec in self:
            _body = (_(
                (
                    "<ul>Advertisement Ended</ul>")
            ))
            for line in rec.advertisement_line_ids:
                line.job_id.message_post(body=_body)
                line.job_id.set_open()
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



class JobPositionCat(models.Model):
    _name = 'advertisement.line'
    _description = 'Advertisement Line'

    allowed_category_id = fields.Many2one('hr.requisition.application', string='Allowed Cat')
    job_id = fields.Many2one('hr.job', string='Job Position')
    branch_id = fields.Many2one('res.branch', string='Branch')
    department_id = fields.Many2one('hr.department', string='Department')
    opening = fields.Integer('Opening')
    sc = fields.Integer('Scheduled Castes')
    general = fields.Integer('General')
    st = fields.Integer('Scheduled Tribes')



class AllowedCategories(models.Model):
    _name = 'allowed.categories'
    _description = 'Allowed Categories'

    allowed_category_id = fields.Many2one('hr.requisition.application', string='Allowed Cat')
    job_id = fields.Many2one('hr.job', string='Job Position')
    vacant_post = fields.Integer('Vacant Post')
    scpercent = fields.Integer('Scheduled Castes')
    generalpercent = fields.Integer('General')
    stpercent = fields.Integer('Scheduled Tribes')
    obcercent = fields.Integer('Other Backward Castes')
    ebcpercent = fields.Integer('Economically Backward Section')
    vhpercent = fields.Integer('Visually Handicapped')
    hhpercent = fields.Integer('Hearing Handicapped')
    phpercent = fields.Integer('Physically Handicapped')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Waiting for approval'),
        ('active', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], default='draft', string='Status', related='allowed_category_id.state')




    @api.constrains('scpercent','generalpercent','stpercent','obcercent','ebcpercent','vhpercent','hhpercent','phpercent',)
    def validate_cat_from_vacancy(self):
        for rec in self:
            if rec.vacant_post and rec.vacant_post > 0:
                if rec.scpercent + rec.generalpercent + rec.stpercent + rec.obcercent + rec.ebcpercent + rec.vhpercent + rec.hhpercent + rec.phpercent <=0:
                    raise ValidationError(
                        _(
                            'Allowed Categories must be greater than 0'))
                if rec.scpercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(Scheduled Castes) must be less than Vacant Post'))
                if rec.generalpercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(General) must be less than Vacant Post'))
                if rec.stpercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(Scheduled Tribes) must be less than Vacant Post'))
                if rec.obcercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(Other Backward Castes) must be less than Vacant Post'))
                if rec.ebcpercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(Economically Backward Section) must be less than Vacant Post'))
                if rec.vhpercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(Visually Handicappped) must be less than Vacant Post'))
                if rec.hhpercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(Hearing Handicapped) must be less than Vacant Post'))
                if rec.phpercent > rec.vacant_post:
                    raise ValidationError(
                        _(
                            'Allowed Category(Physically Handicapped) must be less than Vacant Post'))
