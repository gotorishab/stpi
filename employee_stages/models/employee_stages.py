
from datetime import date
from odoo import models, fields, api,_
from odoo.exceptions import UserError

emp_stages = [
                # ('joined', 'Roll On'),
              # ('grounding', 'Induction'),
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
              ]


class EmployeeFormInherit(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        result = super(EmployeeFormInherit, self).create(vals)
        result.stages_history.sudo().create({'start_date': date.today(),
                                             'employee_id': result.id,
                                             'state': 'test_period'})
        return result

    @api.multi
    def start_grounding(self):
        pass
        # self.state = 'grounding'
        # self.stages_history.sudo().create({'start_date': date.today(),
        #                                    'employee_id': self.id,
        #                                    'state': 'grounding'})

    @api.multi
    def set_as_employee(self):
        self.state = 'employment'
        stage_obj = self.stages_history.search([('employee_id', '=', self.id),
                                                ('state', '=', 'test_period')])
        if stage_obj:
            stage_obj.sudo().write({'end_date': date.today()})
        self.stages_history.sudo().create({'start_date': date.today(),
                                           'employee_id': self.id,
                                           'state': 'employment'})

    @api.multi
    def start_notice_period(self):
        self.state = 'notice_period'
        stage_obj = self.stages_history.search([('employee_id', '=', self.id),
                                                ('state', '=', 'employment')])
        if stage_obj:
            stage_obj.sudo().write({'end_date': date.today()})
        self.stages_history.sudo().create({'start_date': date.today(),
                                           'employee_id': self.id,
                                           'state': 'notice_period'})

    @api.multi
    def relived(self):
        # print("===========check_before_set_as_employee=====================", self.lexit_progress)
        if not self.lexit_progress == 100:
            raise UserError(_("""Please complete Exit process and try again...!"""))
        self.state = 'relieved'
        self.active = False
        stage_obj = self.stages_history.search([('employee_id', '=', self.id),
                                                ('state', '=', 'notice_period')])
        if stage_obj:
            stage_obj.sudo().write({'end_date': date.today()})
        self.stages_history.sudo().create({'end_date': date.today(),
                                           'employee_id': self.id,
                                           'state': 'relieved'})

    @api.multi
    def check_before_set_as_employee(self):
        # print("===========check_before_set_as_employee=====================",self.lentry_progress)
        if not self.lentry_progress == 100:
            raise UserError(_("""Please complete Entry process and try again...!"""))
        return {
            'name': _('Set as Employee'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.employee.stage',
            'view_id':self.env.ref('employee_stages.wizard_employee_form').id,
            'context': {'employee_id':self.id},
            'type': 'ir.actions.act_window',
            'target':'new',
        }


    @api.multi
    def start_test_period(self):
        self.state = 'test_period'
        # self.stages_history.search([('employee_id', '=', self.id),
        #                             ('state', '=', 'grounding')]).sudo().write({'end_date': date.today()})
        self.stages_history.sudo().create({'start_date': date.today(),
                                           'employee_id': self.id,
                                           'state': 'test_period'})

    @api.multi  # added by djay 29/11/2018
    def employee_retired(self):
        self.state = 'retired'
        stage_obj = self.stages_history.search([('employee_id', '=', self.id),
                                                ('state', '=', 'employment')])
        if stage_obj:
            stage_obj.sudo().write({'end_date': date.today()})
        self.stages_history.sudo().create({'start_date': date.today(),
                                           'employee_id': self.id,
                                           'state': 'retired'})
    @api.multi
    def terminate(self):
        self.state = 'terminate'
        self.active = False
        stage_obj = self.stages_history.search([('employee_id', '=', self.id),
                                                ('state', '=', 'employment')])

        if stage_obj:
            stage_obj.sudo().write({'end_date': date.today()})
        else:
            pass
            # self.stages_history.search([('employee_id', '=', self.id),
            #                             ('state', '=', 'grounding')]).sudo().write({'end_date': date.today()})
        self.stages_history.sudo().create({'end_date': date.today(),
                                           'employee_id': self.id,
                                           'state': 'terminate'})

    state = fields.Selection(emp_stages, string='Status', default='test_period', track_visibility='always', copy=False,
                             help="Employee Stages.\nTest period : Probation")
    stages_history = fields.One2many('hr.employee.status.history', 'employee_id', string='Stage History',
                                     help='It shows the duration and history of each stages')
    gratuity_check_no = fields.Char(string='Gratuity check no:')

    reason = fields.Text('Reason')

    state_updated_date =fields.Date('State_updated_state',default=date.today())

    def change_employee_stage(self):
        if self:
            return {
                'name': 'Change Employee stage',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'change.employee.stage',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'view_id': self.env.ref('employee_stages.change_hr_employee_stages_view').id,
                'context': {
                    'default_employee_id': self.id}
            }

class EmployeeStageHistory(models.Model):
    _name = 'hr.employee.status.history'
    _description = 'Status History'

    @api.depends('end_date')
    def get_duration(self):
        for each in self:
            if each.end_date and each.start_date:
                duration = fields.Date.from_string(each.end_date) - fields.Date.from_string(each.start_date)
                each.duration = duration.days

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    duration = fields.Integer(compute=get_duration, string='Duration(days)')
    state = fields.Selection(emp_stages, string='Stage')
    employee_id = fields.Many2one('hr.employee', invisible=1)
    designation_id =fields.Many2one('hr.job','Designation')
    file_no = fields.Char('File No.')
    order_no =fields.Char('Order No.')
    order_date =fields.Date('Order Date')
    Date_wef =fields.Date('Date wef/Extended')
    remarks = fields.Text('Remarks')


class WizardEmployee(models.TransientModel):
    _name = 'wizard.employee.stage'
    _description = 'Wizard employee stage'

    @api.multi
    def set_as_employee(self):
        context = self._context
        employee_obj = self.env['hr.employee'].search([('id', '=', context.get('employee_id'))])
        if self.related_user:
            employee_obj.user_id = self.related_user
        employee_obj.set_as_employee()

    related_user = fields.Many2one('res.users', string="Related User")

class ChangeEmployeeStage(models.TransientModel):
    _name ='change.employee.stage'
    _description = 'Change Employee Stage'

    state = fields.Selection(emp_stages, string='Status',help="Employee Stages.\nTest period : Probation")
    reason = fields.Text('Reason')
    employee_id =fields.Many2one('hr.employee',string='Employee')

    def change_stage(self):
        if self.employee_id:
            emp_id= self.env['hr.employee.status.history'].search([
                                                            ('employee_id','=',self.employee_id.id),
                                                            ('state','=',self.employee_id.state)
                                                           ])
            for emp in  emp_id:
                emp.end_date = date.today()
                emp.get_duration()

            self.employee_id.state = self.state
            self.employee_id.state_updated_date = date.today()
            self.employee_id.stages_history.sudo().create({'start_date': date.today(),
                                                           'employee_id': self.employee_id.id,
                                                           'designation_id':self.employee_id.job_id.id if self.employee_id.job_id else False,
                                                           'state': self.state})


class EmployeeStageConfig(models.Model):
    _name='employee.stage.configuration'
    _description = 'Employee Stage Configuration'

    employee_type = fields.Selection([('regular', 'Regular Employee'),
                                      ('contractual_with_3rd_party', 'Contractual with 3rd Party'),
                                      ('contractual', 'Contractual')], string='Employment Type', required=True)

    recruitment_type = fields.Selection([
                                        ('d_recruitment', 'Direct Recruitment(DR)'),
                                        ('transfer', 'Transfer(Absorption)'),
                                        ('i_absorption', 'Immediate Absorption'),
                                        ('deputation', 'Deputation'),
                                        ('c_appointment', 'Compassionate Appointment'),
                                        ('promotion', 'Promotion'),
                                    ], 'Recruitment Type', required=True)

    existing_state = fields.Selection(emp_stages, string='Existing State',help="Employee Stages.\nTest period : Probation")
    new_state = fields.Selection(emp_stages, string='New State',help="Employee Stages.\nTest period : Probation")
    days =fields.Integer('Days')


    def change_employee_state_cron(self):
        confg = self.env['employee.stage.configuration'].search([])
        for s in confg:
            res = self.env['hr.employee'].search([('employee_type','=',s.employee_type),
                                            ('recruitment_type','=',s.recruitment_type),
                                            ('state','=',s.existing_state)
                                                 ])
            # print("--------------res",res)
            for line in res:
                if (date.today() - line.state_updated_date).days >=s.days:

                    emp_id = self.env['hr.employee.status.history'].search([
                        ('employee_id', '=', line.id),
                        ('state', '=', s.existing_state)
                    ])
                    for emp in emp_id:
                        emp.end_date = date.today()
                        emp.get_duration()

                    line.state = s.new_state
                    line.state_updated_date = date.today()
                    line.stages_history.sudo().create({'start_date': date.today(),
                                                       'employee_id': line.id,
                                                       'designation_id': line.job_id.id if line.job_id else False,
                                                       'state': s.new_state})
