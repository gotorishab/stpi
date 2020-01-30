from odoo import models, fields, api,_

class LeaveTypeEmployeeStages(models.Model):
    _name = 'leave.type.employee.stage'
    _description = 'Leave Type employee stage Changes For STPI'
    _rec_name = 'name'
    
    name = fields.Char(string="Name")
    tech_name = fields.Selection([('joined', 'Roll On'),
                              ('grounding', 'Induction'),
                              ('test_period', 'Probation'),
                              ('employment', 'Employment'),
                              ('notice_period', 'Notice Period'),
                              ('relieved', 'Resigned'),
                              ('terminate', 'Terminated'),
                              ('retired','Retired'),
                              ('suspended','Suspended'),
                              ('superannuation','Superannuation'),
                              ('deceased','Deceased'),
                              ('absconding','Absconding'),
                            ],string="Name")
