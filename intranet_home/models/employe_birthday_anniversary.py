from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    marriage_anniversary = fields.Date(string='Marriage Anniversary')
    work_anniversary = fields.Date(string='Work Anniversary')
    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')

    def action_wish_scheduler(self):
        employee_ids = self.env['hr.employee'].search([])
        current_date = datetime.now().date()
        mail_mail = request.env['mail.mail'].sudo()
        email_from = request.env.user.login or ''
        for rec in employee_ids:
            email_to =  rec.work_email
            if rec.marriage_anniversary and rec.marriage_anniversary == current_date:
                anniversarymail_obj = self.env['vardhman.employee.anniversarymail'].search([('name', '=', 'marriage')], limit=1)
                if anniversarymail_obj:
                    body = anniversarymail_obj.email
                    body = body.replace("$[employee_name]", rec.name)
                    mail_values = {
                        'email_from': email_from,
                        'email_to':email_to,
                        'subject': anniversarymail_obj.title,
                        'body_html': body,
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send()
            if rec.birthday and rec.birthday == current_date:
                anniversarymail_obj = self.env['vardhman.employee.anniversarymail'].search([('name', '=', 'birthday')], limit=1)
                if anniversarymail_obj:
                    body = anniversarymail_obj.email
                    body = body.replace("$[employee_name]", rec.name)
                    mail_values = {
                        'email_from': email_from,
                        'email_to':email_to,
                        'subject': anniversarymail_obj.title,
                        'body_html': body,
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send()
            if rec.work_anniversary and rec.work_anniversary == current_date:
                anniversarymail_obj = self.env['vardhman.employee.anniversarymail'].search([('name', '=', 'work')], limit=1)
                if anniversarymail_obj:
                    body = anniversarymail_obj.email
                    body = body.replace("$[employee_name]", rec.name)
                    mail_values = {
                        'email_from': email_from,
                        'email_to':email_to,
                        'subject': anniversarymail_obj.title,
                        'body_html': body,
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send()


class VardhmanEmployeeBirthday(models.Model):
    _name = "vardhman.employee.birthday"
    _description = "Vardhman Employee Birthday"

    name = fields.Char(string="Name", store=True)
    image = fields.Image(string="Image", store=True)
    job_title = fields.Char(string="Job Title", store=True)
    birthday = fields.Date(string='Date of Birth')


    def button_create_activities(self):
        self.ensure_one()
        serch_id = self.env['ir.model'].search([('model', '=', 'vardhman.employee.birthday')])
        compose_form_id = self.env.ref('mail.mail_activity_view_form_popup').id

        ctx = dict(
            default_res_id=self.id,
            default_res_model_id=serch_id.id,
            default_user_id=self.env.user.id,
            date_deadline=datetime.now().date(),
            activity_type_id=2
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


class VardhmanEmployeeMarriageAniversary(models.Model):
    _name = "vardhman.employee.marriageanniversary"
    _description = "Vardhman Employee Marriage Anniversary"

    name = fields.Char(string="Name", store=True)
    image = fields.Binary(string="Image", store=True)
    job_title = fields.Char(string="Job Title", store=True)
    marriage_anniversary = fields.Date(string='Marriage Anniversary')


    def button_create_activities(self):
        self.ensure_one()
        serch_id = self.env['ir.model'].search([('model', '=', 'vardhman.employee.birthday')])
        compose_form_id = self.env.ref('mail.mail_activity_view_form_popup').id

        ctx = dict(
            default_res_id=self.id,
            default_res_model_id=serch_id.id,
            default_user_id=self.env.user.id,
            date_deadline=datetime.now().date(),
            activity_type_id=2
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

class VardhmanEmployeeWorkAniversary(models.Model):
    _name = "vardhman.employee.workanniversary"
    _description = "Vardhman Employee Work Anniversary"

    name = fields.Char(string="Name", store=True)
    image = fields.Image(string="Image", store=True)
    job_title = fields.Char(string="Job Title", store=True)
    work_anniversary = fields.Date(string='Work Anniversary')



    def button_create_activities(self):
        self.ensure_one()
        serch_id = self.env['ir.model'].search([('model', '=', 'vardhman.employee.birthday')])
        compose_form_id = self.env.ref('mail.mail_activity_view_form_popup').id

        ctx = dict(
            default_res_id=self.id,
            default_res_model_id=serch_id.id,
            default_user_id=self.env.user.id,
            date_deadline=datetime.now().date(),
            activity_type_id=2
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

class VardhmanEmployeeMail(models.Model):
    _name = "vardhman.employee.anniversarymail"
    _description = "Vardhman Employee Mail Anniversary"

    name = fields.Selection([
        ('birthday', 'Birth Anniversary'),
        ('work', 'Work Anniversary'),
        ('marriage', 'Marriage Anniversary')
    ], string='Name')

    email = fields.Html(string="E-Mail", default="$[employee_name]")
    title = fields.Char(string="Title")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('mail_sent', 'Mail Sent'),
    ], string='state',default='draft')



    def button_create_activities(self):
        employee_ids = self.env['hr.employee'].search([])
        current_date = datetime.now().date()
        mail_mail = request.env['mail.mail'].sudo()
        email_from = request.env.user.login or ''
        for rec in employee_ids:
            email_to =  rec.work_email
            if self.name == 'marriage' and rec.marriage_anniversary and rec.marriage_anniversary == current_date:
                anniversarymail_obj = self
                if anniversarymail_obj:
                    body = anniversarymail_obj.email
                    body = body.replace("$[employee_name]", rec.name)
                    mail_values = {
                        'email_from': email_from,
                        'email_to':email_to,
                        'subject': anniversarymail_obj.title,
                        'body_html': body,
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send()
            if self.name == 'birthday' and rec.birthday and rec.birthday == current_date:
                anniversarymail_obj = self
                if anniversarymail_obj:
                    body = anniversarymail_obj.email
                    body = body.replace("$[employee_name]", rec.name)
                    mail_values = {
                        'email_from': email_from,
                        'email_to':email_to,
                        'subject': anniversarymail_obj.title,
                        'body_html': body,
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send()
            if self.name == 'work' and rec.work_anniversary and rec.work_anniversary == current_date:
                anniversarymail_obj = self
                if anniversarymail_obj:
                    body = anniversarymail_obj.email
                    body = body.replace("$[employee_name]", rec.name)
                    mail_values = {
                        'email_from': email_from,
                        'email_to':email_to,
                        'subject': anniversarymail_obj.title,
                        'body_html': body,
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send()
        self.write({'state': 'mail_sent'})

