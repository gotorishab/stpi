from odoo import api, fields, models, _
from odoo.http import request
from datetime import date


class HealthBusinessType(models.Model):
    _name = "health.manage.safetyobs"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Health Manage Safety Committee Meeting"


    observer_name = fields.Char('Observer Name :')
    plant = fields.Char('Plant :')
    date = fields.Date('Date :')
    department_id = fields.Many2one('hr.department :')
    Observed_name = fields.Char('Observed Name :')

    housekeeping = fields.Boolean('Housekeeping')
    dress = fields.Boolean('Dress Code(Hair,Jewelry,Etc.)')
    pre = fields.Boolean('PRE (earplugs, gloves, face shield, etc.)')
    chemical = fields.Boolean('Chemical use/storage/labels')
    debris = fields.Boolean('Debris/waste (floor, hand, etc.)')
    knife = fields.Boolean('Knife safety (lap ups, glove, knife)')
    machine = fields.Boolean('Machine guarding & safety interlocks')
    loto = fields.Boolean('LOTO (following procedures, using locks 7 tags, etc.)')
    manual = fields.Boolean('Manual material handling (lifting, pulling, pushing)')
    slip = fields.Boolean('Slip/trips/falls conditions (spills, boxes, etc.)')
    ergonomic = fields.Boolean('Ergonomic position (reaching, weight, height, etc.)')
    not_sec = fields.Boolean('Not In assigned area/Security')
    emergency_access = fields.Boolean('Emergency access/egress')
    other_behave = fields.Boolean('Other behavior: list')
    other_behave_ex = fields.Char('Other')
    unsafe_act = fields.Boolean('UNSAFE ACT')
    unsafe_act_ex = fields.Char('Other')
    potential_hazard = fields.Char('What were potential hazard? :')
    unsafe_other = fields.Char('What questions did you asked to better understand 1/11, situation/condition')
    question_sit = fields.Char('What alternative behavior did you suggest or request to redirect the unsafe act? :')
    commitment_follow = fields.Char('What commitment did you gain 0 how are to going to follow up? :')



    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancelled', 'Cancelled')
         ], required=True, default='draft', string='Status', track_visibility='always')

    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def button_submit(self):
        for rec in self:
            rec.write({'state': 'submitted'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})
