# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request


class HRApplicant(models.Model):
    _inherit = "hr.applicant"

    applicant_ref_id = fields.Char("Reference No.", copy=False)

    @api.model
    def create(self, vals):
        if vals.get('applicant_ref_id', 'New') == 'New':
            vals['applicant_ref_id'] = self.env['ir.sequence'].next_by_code('hr.applicant') or 'New'
        result = super(HRApplicant, self).create(vals)
        return result
