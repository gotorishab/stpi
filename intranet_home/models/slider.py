# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request


class VardhmanUsefulLinks(models.Model):
    _name = "vardhman.slider.links"
    _description = "vardhman Slider links"

    name = fields.Char(string="Name", store=True)
    mid_date = fields.Char(string="Data", store=True)
    url = fields.Char(string="URL", store=True)
    icon = fields.Binary(string="Image", store=True)


class VardhmanMagazineLinks(models.Model):
    _name = "vardhman.magazine.links"
    _description = "vardhman Magazine links"

    url = fields.Char(string="URL", store=True)
    icon = fields.Binary(string="Image", store=True)


class VardhmanPhotoLinks(models.Model):
    _name = "vardhman.photo.links"
    _description = "vardhman Magazine links"

    url = fields.Char(string="URL", store=True)
    icon = fields.Binary(string="Image", store=True)


class VardhmanVideosLinks(models.Model):
    _name = "vardhman.videos.links"
    _description = "vardhman Magazine links"

    url = fields.Char(string="URL", store=True)
    icon = fields.Binary(string="Video", store=True)
