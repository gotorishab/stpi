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
            self.abap_id.button_approved()
            self.update({"state":"self_review"})

    def button_reject(self):
        if self.abap_id:
            self.abap_id.button_reject()
            self.update({"state":"rejected"})


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
