from datetime import date
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class Empstatus_inh(models.Model):
    _inherit = 'hr.employee.status.history'

    effective_date = fields.Date('Effective Date')
    ndc_upload = fields.Binary('No Due Certificate')


class EmpStage_inh(models.TransientModel):
    _inherit = 'change.employee.stage'

    file_no = fields.Char('File No.')
    order_no =fields.Char('Order No.')
    order_date =fields.Date('Order Date')
    Date_wef =fields.Date('Date wef/Extended')
    remarks = fields.Text('Remarks')
    effective_date = fields.Date('Effective Date')
    ndc_upload = fields.Binary('No Due Certificate')

    def change_stage(self):
        if self.employee_id:
            emp_id = self.env['hr.employee.status.history'].search([
                ('employee_id', '=', self.employee_id.id),
                ('state', '=', self.employee_id.state)
            ])
            for emp in emp_id:
                emp.end_date = date.today()
                emp.get_duration()

            self.employee_id.state = self.state
            self.employee_id.state_updated_date = date.today()
            self.employee_id.stages_history.sudo().create({'start_date': date.today(),
                                                           'employee_id': self.employee_id.id,
                                                           'designation_id': self.employee_id.job_id.id if self.employee_id.job_id else False,
                                                           'state': self.state,
                                                           'order_no': self.order_no if self.order_no else False,
                                                           'order_date': self.order_date if self.order_date else False,
                                                           'file_no': self.file_no if self.file_no else False,
                                                           'Date_wef': self.Date_wef if self.Date_wef else False,
                                                           'effective_date': self.effective_date if self.effective_date else False,
                                                           'ndc_upload': self.ndc_upload if self.ndc_upload else False,
                                                           'remarks': self.remarks if self.remarks else False,
                                                           })