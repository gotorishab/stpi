# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime


class ResUsers(models.Model):
    _inherit = "res.users"

    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')
    department_id = fields.Many2one('hr.department',string='Department')
    business_type = fields.Many2one('vardhman.businesstype.master',string='Business Type')
    description = fields.Html('Description')




class ResGroups(models.Model):
    _inherit = "res.groups"

    # @api.model
    # def create(self, values):
    #     user = super(ResGroups, self).create(values)
    #     print('===============================')
    #     # if self:
    #     grp = self.env['mail.channel'].sudo().create({
    #         'name': str(self.name),
    #         'public': 'public',
    #         # 'group_public_id': self.id,
    #     })
    #     print('===============================',grp)
    #
    #
    #     # self._update_user_groups_view()
    #     # actions.get_bindings() depends on action records
    #     # self.env['ir.actions.actions'].clear_caches()
    #     return user


    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')
    department_id = fields.Many2one('hr.department',string='Department')
    business_type = fields.Many2one('vardhman.businesstype.master',string='Business Type')


