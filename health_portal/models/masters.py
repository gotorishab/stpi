from odoo import api, fields, models, _
from odoo.http import request


class HealthBusinessType(models.Model):
    _name = "health.business.type"
    _description = "Health Business Type"

    name = fields.Char('Business Type:')
    description = fields.Text('Process Description :')


class HealthUnitMaster(models.Model):
    _name = "health.unit.master"
    _description = "Health Unit Master"

    name = fields.Char('Unit Name:')
    location = fields.Char('Unit Location:')
    description = fields.Text('Unit Description :')



class HealthSectionMaster(models.Model):
    _name = "health.section.master"
    _description = "Health Section Master"

    name = fields.Char('Section Name:')
    description = fields.Text('Section Description :')




class HealthIncidentReason(models.Model):
    _name = "health.incident.master"
    _description = "Health Incident Reason :"

    name = fields.Char('Incident Reason :')
    description = fields.Text('Section Description :')



class HealthDepartmentSection(models.Model):
    _name = "health.department.section"
    _description = "Health Department Section :"

    department_id = fields.Many2one('hr.department', string='Select Department :')
    section_id = fields.Many2one('health.section.master', string='Select Section :')



class HealthBusinessUnit(models.Model):
    _name = "health.business.unit"
    _description = "Health Business Unit :"

    business_id = fields.Many2one('health.business.type', string='Select Business Name :')
    unit_id = fields.Many2one('health.unit.master', string='Select Unit Name :')




class HealthAccidentReason(models.Model):
    _name = "health.accident.master"
    _description = "Health Accident Reason :"

    name = fields.Char('Incident Reason :')
    description = fields.Text('Reason Description :')





class HealthAuditTypeMaster(models.Model):
    _name = "health.audit.type.master"
    _description = "Health Audit Type Reason :"
    _rec_name = "audit_type"


    audit_type = fields.Char('Audit Type :')
    frequency = fields.Char('Frequency :')
    objective = fields.Many2many('health.audit.objective',string='Objective')
    introduction = fields.Text('Introduction :')
    checklist_ids = fields.One2many('health.audit.checklist', 'audit_type_id', string='Checklist')


class HealthAuditObjective(models.Model):
    _name = "health.audit.objective"
    _description = "Health Audit Objective :"

    name = fields.Char('Name')


class HealthAuditChecklist(models.Model):
    _name = "health.audit.checklist"
    _description = "Health Audit Checklist :"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')





class HealthAmmoniaAafetyAudit(models.Model):
    _name = "health.ammonia.safety.audit"
    _description = "Health Ammonia safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')



class HealthCanteenAafetyAudit(models.Model):
    _name = "health.canteen.safety.audit"
    _description = "Health Canteen safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')



class HealthCPPAafetyAudit(models.Model):
    _name = "health.cpp.safety.audit"
    _description = "Health CPP safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')




class HealthGodownAafetyAudit(models.Model):
    _name = "health.godown.safety.audit"
    _description = "Health Go-Down safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')




class HealthHostelAafetyAudit(models.Model):
    _name = "health.hostel.safety.audit"
    _description = "Health hostel safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')




class HealthHplantAafetyAudit(models.Model):
    _name = "health.hplant.safety.audit"
    _description = "Health hplant safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')




class HealthWashroomAafetyAudit(models.Model):
    _name = "health.washroom.safety.audit"
    _description = "Health washroom safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')




class HealthWorkplaceAafetyAudit(models.Model):
    _name = "health.workplace.safety.audit"
    _description = "Health workplace safety audit"

    audit_type_id = fields.Many2one('health.audit.type.master',string='Select Audit Type :')
    checklist_item = fields.Char('Checklist Item :')
    sub_checklist_item = fields.Char('Sub Checklist Item :')

