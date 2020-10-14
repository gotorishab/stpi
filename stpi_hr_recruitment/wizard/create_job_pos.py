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
            pass