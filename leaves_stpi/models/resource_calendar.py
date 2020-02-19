from odoo import models, fields, api
from datetime import time, datetime,timedelta
from datetime import date, datetime

class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'
    _description= ' Resource Calendar Branch'
    
    branch_id = fields.Many2one('res.branch',string="Branch",required=True)
    
    @api.multi
    def allow_public_holiday_on_caledar(self):
        for resource in self:
            employee_ids = self.env['hr.employee'].search([('branch_id','=',resource.branch_id.id)])
            for employee in employee_ids:
                employee.resource_calendar_id = self.id
                
                
class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar.leaves'
    _description= ' Resource Calendar Leaves'
    
    date = fields.Date(string="Date",required=True)
    
    @api.onchange('date')
    def onchange_date(self):
        a = time()
        b = time(23, 56, 56)
        for line in self:
            if line.date:
                entered_date = datetime.strptime(str(line.date), '%Y-%m-%d')
#                 print("??????????????????????",entered_date)
                line.date_from = entered_date - timedelta(hours=5,minutes=30,seconds=00)
                line.date_to = entered_date + timedelta(hours=18,minutes=28,seconds=58)
                
                
                