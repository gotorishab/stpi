from odoo import api, fields, models, tools, _
from datetime import datetime, date


class HREmployeeProperty(models.Model):
    _name = "hr.employee.property"
    _description = "HR Property Form-II"

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    employee_id = fields.Many2one('hr.employee', string="Name of the Government servant", default=_default_employee,track_visibility='always')
    designation = fields.Many2one('hr.job',string="Designation: ")

    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def get_designation(self):
        for rec in self:
            rec.designation = rec.employee_id.job_id.id
            rec.employee_no = rec.employee_id.identify_id
            emp_contract = self.env['hr.contract'].search(
                [('employee_id', '=', rec.employee_id.id), ('state', '=', 'open')], limit=1)
            if emp_contract:
                for contract in emp_contract:
                    rec.scale_pay = contract.wage
                    rec.pay_level_id = contract.pay_level_id.id


    service_belo = fields.Char("Service to which belongs: ",track_visibility='always')
    employee_no = fields.Char(string="Employee No./Code No.: ")

    pay_level_id = fields.Many2one('hr.payslip.paylevel', string='Pay Level	',track_visibility='always')
    scale_pay = fields.Float("Present pay:",track_visibility='always')

    purpose = fields.Char("Purpose of application:", track_visibility='always')

    #Description of Movable Property
    propert_ad = fields.Selection([('acquisition', 'Acquisition'), (' disposal', ' Disposal')], string='Acquisition or disposal',track_visibility='onchange')
    acq_date = fields.Date(string="Date of acquisition or disposal")
    details_property = fields.Char(string="Details of Property" )
    mode_of_acquisition = fields.Selection(
        [('pursale', 'Purchase/Sale'), ('gift', 'Gift'), ('Motagage', 'Motagage'), ('Lease', 'Lease'),
         ('Other', 'Other')
         ], string='Mode of acquistion', track_visibility='onchange')
    full_part = fields.Char("Whether the applicants interest in the property is in full or part")
    owner_property = fields.Char("Ownership of the property")
    property_price = fields.Float("Sale/Purchase price of the property")

    acquisition_source = fields.Selection(
        [('p_s', 'Personal Savings'), ('others', 'Others')
         ], string='In case of acquistion, source or sources from which financed/propsed to be financed',
        track_visibility='onchange')
    copy_attached = fields.Char('In the case of disposal of property, was requisite sanction/intimation obtained/given for its acquisition (A copy of the sanction/acknowledgement should be attached):')

    #Details of the Parties with whom transaction is proposed to be made! has been made:

    address_details = fields.Char("Name and address of the parties. ")
    party_relation = fields.Boolean('Is the party related to the applicant? If so, state the relationship.')
    state_relationship = fields.Char(string="state relationship")
    dealings = fields.Char(string="Did the applicant have any official dealing with the parties?")
    official_party = fields.Char(string="Nature of official dealing with the party")
    transaction = fields.Char(string="How was transaction arranged?")

    acquistion_gift = fields.Boolean(string="In the case of acquistion by gifts, whether sanction is also required under rule 13 of CCS Rules. 1964",track_visibility='onchange')
    rel_fact = fields.Char(string="Any other relevant fact which the appliciant may like to mention",track_visibility='onchange')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', string='Status', track_visibility='onchange')



    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})


    @api.multi
    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'submitted'})

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})