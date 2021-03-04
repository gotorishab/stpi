from odoo import api, fields, models, tools, _
from datetime import datetime, date


class HRPropertyNew(models.Model):
    _name = "hr.property.new"
    _description = "HR Property Form-I"

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    employee_id = fields.Many2one('hr.employee', string="Name of the Government servant", default=_default_employee,track_visibility='always')
    designation = fields.Many2one('hr.job',string="Designation: ")

    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def get_designation(self):
        for rec in self:
            rec.designation = rec.employee_id.job_id.id
            # print('=================identify_id=================',rec.employee_id.identify_id)
            rec.employee_no = rec.employee_id.identify_id
            # rec.scale_pay = rec.employee_id.pay_level_id.id


    service_belo = fields.Char("Service to which belongs: ",track_visibility='always')
    employee_no = fields.Many2one(string="Employee No./Code No.: ")

    # scale_pay = fields.Many2one("hr.payslip.paylevel", string="Scale of Pay and present pay:",track_visibility='always')
    scale_pay = fields.Float("Scale of Pay and present pay:",track_visibility='always')
    purpose = fields.Char("Purpose of application:",track_visibility='always')
    propert_ad = fields.Selection([('acquired', 'Acquired'), ('disposed', 'Disposed')], string='Whether property is being acquired or disposed of',track_visibility='onchange')
    probable_date = fields.Date(string='Probable date of acquistion or disposal of property',track_visibility='onchange')
    mode_of_acquisition = fields.Selection(
        [('pursale', 'Purchase/Sale'), ('gift', 'Gift'), ('Motagage', 'Motagage'), ('Lease', 'Lease'),
         ('Other', 'Other')
         ], string='Mode of acquistion', track_visibility='onchange')

    #Description of Property
    address_details = fields.Char("Full details about location")
    des_property = fields.Char(string="Description of the Property")
    free_leas_hold = fields.Char("Whether freehold or leasehold")
    full_part = fields.Char("Whether the applicants interest in the property is in full or part")
    owner_property = fields.Char("Ownership of the property")
    property_price = fields.Float("Sale/Purchase price of the property")

    acquisition_source = fields.Selection(
        [('p_s', 'Personal Savings'), ('others', 'Others')
         ], string='In case of acquistion, source or sources from which financed/propsed to be financed',
        track_visibility='onchange')
    copy_attached = fields.Char('In the case of disposal of property, was requisite sanction/intimation obtained/given forits acquisition (A copy of the sanction/acknowledgement should be attached):')

    #. Details of the Parties with whom transaction is proposed to be made:

    party_details = fields.Char('Name and address of the party whith whom transaction is proposed to be made')
    party_relation = fields.Boolean('Is the party related to the applicant? If so, state the relationship.')
    state_relationship = fields.Char(string="state relationship")
    dealings = fields.Char(string="Did the applicant have any official dealing with the parties?")
    transaction = fields.Char(string="How was transaction arranged?")

    acquistion_gift = fields.Boolean(string="In the case of acquistion by gifts, whether sanction is also required under rule 13 of CCS Rules. 1964",track_visibility='onchange')
    rel_fact = fields.Char(string="Any other relevant fact which the appliciant may like to mention",track_visibility='onchange')

    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')
         ], required=True, default='draft', string='Status', track_visibility='onchange')


