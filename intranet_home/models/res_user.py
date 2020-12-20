# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime


class ResUsers(models.Model):
    _inherit = "res.users"

    unit_id = fields.Many2one('vardhman.unit.master',string='Unit')
    department_id = fields.Many2one('hr.department',string='Department')