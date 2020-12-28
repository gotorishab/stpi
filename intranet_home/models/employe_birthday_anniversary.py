# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    marriage_anniversary = fields.Date(string='Marriage Anniversary')
    work_anniversary = fields.Date(string='Work Anniversary')
    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')


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
