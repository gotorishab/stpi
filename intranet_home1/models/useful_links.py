# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request


class VardhmanUsefulLinks(models.Model):
    _name = "vardhman.useful.links"
    _description = "vardhman useful links"

    name = fields.Char(string="Name", store=True)
    url = fields.Char(string="URL", store=True)
    icon = fields.Binary(string="Icon", store=True)
