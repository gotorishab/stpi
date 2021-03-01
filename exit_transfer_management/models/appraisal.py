from odoo import models, fields, api

#Appraisal Request
class PendingAppraisalRequest(models.Model):
    _name = "pending.appraisal.request"
    _description = "Pending Appraisal Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    abap_id = fields.Many2one('appraisal.main', string='APAR Period')
    template_id = fields.Many2one('appraisal.main',string ='Template Id')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'),
                              ('reporting_authority_review', 'Reporting Authority Reviewed'),
                              ('reviewing_authority_review', 'Reviewing Authority Reviewed'),
                              ('completed', 'Completed'), ('raise_query', 'Raise Query'), ('rejected', 'Rejected')])

    def button_self_reviewed(self):
        if self.abap_id:
            self.abap_id.sudo().button_approved()
            self.state = self.abap_id.state
            me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            self.env['exit.management.report'].sudo().create({
                "exit_transfer_id": self.exit_transfer_id.id,
                "employee_id": self.exit_transfer_id.employee_id.id,
                "exit_type": self.exit_transfer_id.exit_type,
                "module": 'Appraisal',
                "module_id": str(self.abap_id.id),
                "action_taken_by": (me.id),
                "action_taken_on": (self.employee_id.id)
            })
            self.sudo().unlink()

    def button_reject(self):
        if self.abap_id:
            self.abap_id.sudo().button_reject()
            self.state = self.abap_id.state
            me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            self.env['exit.management.report'].sudo().create({
                "exit_transfer_id": self.exit_transfer_id.id,
                "employee_id": self.exit_transfer_id.employee_id.id,
                "exit_type": self.exit_transfer_id.exit_type,
                "module": 'Appraisal',
                "module_id": str(self.abap_id.id),
                "action_taken_by": (me.id),
                "action_taken_on": (self.employee_id.id)
            })
            self.sudo().unlink()


class SubmittedAppraisalRequest(models.Model):
    _name = "submitted.appraisal.request"
    _description = "Submitted Appraisal Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    abap_id = fields.Many2one('appraisal.main', string='APAR Period')
    template_id = fields.Many2one('appraisal.main',string ='Template Id')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'),
                              ('reporting_authority_review', 'Reporting Authority Reviewed'),
                              ('reviewing_authority_review', 'Reviewing Authority Reviewed'),
                              ('completed', 'Completed'), ('raise_query', 'Raise Query'), ('rejected', 'Rejected')])

    def button_cancel(self):
        if self.abap_id:
            self.abap_id.sudo().button_reject()
            self.state = self.abap_id.state
            me = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            self.env['exit.management.report'].sudo().create({
                "exit_transfer_id": self.exit_transfer_id.id,
                "employee_id": self.exit_transfer_id.employee_id.id,
                "exit_type": self.exit_transfer_id.exit_type,
                "module": 'Appraisal',
                "module_id": str(self.abap_id.id),
                "action_taken_by": (me.id),
                "action_taken_on": (self.employee_id.id)
            })
            self.sudo().unlink()


class UpcomingAppraisalRequest(models.Model):
    _name = "upcoming.appraisal.request"
    _description = "Upcoming Appraisal Request"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By')
    abap_id = fields.Many2one('appraisal.main', string='APAR Period')
    template_id = fields.Many2one('appraisal.main', string='Template Id')
    state = fields.Selection([('draft', 'Draft'), ('self_review', 'Self Reviewed'),
                              ('reporting_authority_review', 'Reporting Authority Reviewed'),
                              ('reviewing_authority_review', 'Reviewing Authority Reviewed'),
                              ('completed', 'Completed'), ('raise_query', 'Raise Query'), ('rejected', 'Rejected')])
