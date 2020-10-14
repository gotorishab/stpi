from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
from datetime import datetime


class CreateJobPos(models.TransientModel):
    _name = 'create.jobrecruit.line'
    _description = 'Job Opening'


    advertisement_id = fields.Many2one('hr.requisition.application', invisible=1)
    job_recruit = fields.Many2many('recruitment.jobop')



    def confirm_job_pos(self):
        if self:
            pf_details_ids = []
            for line in self.jo
            pf_details_ids.append((0, 0, {
                'allowed_category_id': self.advertisement_id.id,
                'job_id': record.employee_id.id,
                'branch_id': record.employee_id.id,
                'category_id': record.employee_id.id,
                'state': record.employee_id.id,
                'employee_type': 'Deposit',
                'remarks': 'Deposit',
                'opening': 'Deposit',
            }))
            record.pf_details_ids = pf_details_ids