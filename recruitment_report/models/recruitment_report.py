from odoo import fields,api,models
import math
from datetime import datetime, timedelta
from pytz import timezone, UTC


class LateComingReport(models.Model):
    _name="recruitment.report"
    _description="Recruitment Report"



    x_jobposition = fields.Char(string="Job Position")
    x_department = fields.Char(string="Department")
    x_branch = fields.Char(string="Branch")
    x_sanctionedpositions = fields.Integer(string="Sanctioned Positions")
    x_currentempcount = fields.Integer(string="Current EMP count")
    x_scpercet = fields.Float(string="SC Percent")
    x_stpercet = fields.Float(string="ST Percent")
    x_obcpercet = fields.Float(string="OBC Percent")
    x_ebcpercet = fields.Float(string="EBC Percent")
    x_vhpercent = fields.Float(string="VH Percent")
    x_phpercent = fields.Float(string="PH Percent")
    x_hhpercent = fields.Float(string="HH Percent")
    x_ruleclass = fields.Char(string="Rule Class")
    x_nosc = fields.Float(string="No SC")
    x_nost = fields.Float(string="No ST")
    x_noobc = fields.Float(string="No OBC")
    x_noebc = fields.Float(string="No EBC")
    x_currobc = fields.Float(string="Current OBC")
    x_currgen = fields.Float(string="Current General")
    x_currsc = fields.Float(string="Current SC")
    x_currst = fields.Float(string="Current ST")
    x_currewc = fields.Float(string="Current EWC")


    def get_recruitment_report(self):
        return self.env['recruitment.report'].search([])

