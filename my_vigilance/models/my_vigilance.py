from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
import re
from datetime import datetime

class MyVigilance(models.Model):
    _name = "my.vigilance"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Vigilance"

    def default_country(self):
        return self.env['res.country'].search([('name', '=', 'India')], limit=1)

    vigilance_sequence = fields.Char('Vigilance number')
    reg_no = fields.Char(string = 'Registration number',track_visibility='always')
    name = fields.Char(string="Case Name",track_visibility='always')
    date_of_receipt = fields.Date(string="Date of Receipt", default=fields.Date.today(),track_visibility='always')
    address = fields.Char(string="Address",track_visibility='always')
    district = fields.Char(string="District",track_visibility='always')

    state_id = fields.Many2one("res.country.state", string='State', help='Enter State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', help='Select Country', ondelete='restrict', default=default_country)

    mobile = fields.Char(string="Mobile",track_visibility='always')
    email = fields.Char(string="Email",track_visibility='always')
    description = fields.Text(string="Description",track_visibility='always')
    org_name = fields.Char(string="  Name of Organization(s) where Grievance is pending",track_visibility='always')
    receipt_type = fields.Many2one('vigilance.receipt.type', string="Receipt Type",track_visibility='always')
    remarks = fields.Text('Remarks')


    state = fields.Selection([('draft', 'Draft'), ('in_progress', 'In-Progress'), ('closed', 'Closed')], required=True, string='Status', default='draft', track_visibility='always')



    @api.multi
    def button_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.multi
    def button_in_progress(self):
        for rec in self:
            rec.write({'state': 'in_progress'})

    @api.multi
    def button_re_open(self):
        for rec in self:
            rec.button_in_progress()

    @api.multi
    def button_register_actions(self):
        rc = {
            'name': 'Register actions',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('my_vigilance.view_reason_revert_vigilance_wizard').id,
            'res_model': 'revert.vigilance.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
            }
        }
        return rc

    @api.multi
    def button_create_activities(self):
        self.ensure_one()
        serch_id = self.env['ir.model'].search([('model', '=', 'my.vigilance')])
        compose_form_id = self.env.ref('mail.mail_activity_view_form_popup').id

        ctx = dict(
            default_res_id=self.id,
            default_res_model_id=serch_id.id,
            default_user_id=self.env.user.id,
            date_deadline=datetime.now().date(),
            activity_type_id=4
        )
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


    @api.model
    def create(self, vals):
        res =super(MyVigilance, self).create(vals)
        sequence = ''
        seq = self.env['ir.sequence'].next_by_code('my.vigilance')
        sequence = 'Vigilance - ' + str(seq)
        res.vigilance_sequence = sequence
        return res

    @api.multi
    @api.depends('vigilance_sequence')
    def name_get(self):
        res = []
        for record in self:
            if record.vigilance_sequence:
                name = record.vigilance_sequence
            else:
                name = 'Vigilance'
            res.append((record.id, name))
        return res


    @api.multi
    def button_closed(self):
        for rec in self:
            rec.write({'state': 'closed'})

    @api.constrains('email')
    @api.onchange('email')
    def _check_email_address(self):
        for rec in self:
            if rec.email:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',rec.email)
                if match == None:
                    raise ValidationError(_("Please enter correct Email Address..."))




    @api.constrains('mobile')
    @api.onchange('mobile')
    def _check_mobile_number(self):
        for rec in self:
            if rec.mobile:
                for e in rec.mobile:
                    if not e.isdigit():
                        raise ValidationError(_("Please enter correct Mobile number, it must be numeric..."))
                if len(rec.mobile) != 10:
                    raise ValidationError(_("Please enter correct Mobile number, it must be of 10 digits..."))




    @api.constrains('name')
    @api.onchange('name')
    def _check_name_number(self):
        for rec in self:
            if rec.name:
                for e in rec.name:
                    if not e.isalpha():
                        raise ValidationError(_("Please enter correct Name, it must be Character only..."))
                if len(rec.name) > 120:
                    raise ValidationError(_("Please enter correct Name, it must be greater than 120 alphabet..."))



    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}




class ReceiptType(models.Model):

    _name = "vigilance.receipt.type"
    _description = "Vigilance Receipt Type"

    name = fields.Char('Name')