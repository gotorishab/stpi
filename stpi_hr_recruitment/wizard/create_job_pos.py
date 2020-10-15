from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
from datetime import datetime


class CreateJobPos(models.TransientModel):
    _name = 'create.jobrecruit.line'
    _description = 'Job Opening'


    advertisement_id = fields.Many2one('hr.requisition.application', invisible=1)
    job_recruit = fields.Many2many('recruitment.jobop', string='Job Openings')



    def confirm_job_pos(self):
        if self:
            # pass
            advertisement_line_ids = []
            for line in self.job_recruit:
                for inline in line.job_pos:
                    advertisement_line_ids.append((0, 0, {
                        'allowed_category_id': self.advertisement_id.id,
                        'job_id': inline.job_id.id,
                        'branch_id': inline.branch_id.id,
                        'category_id': inline.category_id.id,
                        'state': inline.category_id.id,
                        'remarks': inline.remarks,
                        'opening': 1,
                    }))
                line.write({'state': 'published'})
            self.advertisement_id.advertisement_line_ids = advertisement_line_ids