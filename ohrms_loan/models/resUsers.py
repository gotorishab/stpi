# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class resUsers(models.Model):
    _inherit = 'res.users'


    @api.model
    def default_get(self, field_list):
        result = super(resUsers, self).default_get(field_list)
        result['tz'] = 'Asia/Kolkata'
        return result

    @api.model
    def create(self, vals):
        res = super(resUsers, self).create(vals)
        res.tz = 'Asia/Kolkata'
        return res
