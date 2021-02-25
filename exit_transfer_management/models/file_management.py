from odoo import models, fields, api


# File management
class CorrespondenceExitManagement(models.Model):
    _name = "correspondence.exit.management"
    _description = "Correspondence Exit Management"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    correspondence_id = fields.Many2one('muk_dms.file', string='Correspondence')
    letter_no = fields.Char(string="Letter Number")
    file_assign_id = fields.Many2one('folder.master', string="File Assigned")

    def correspondence_forward(self):
        pass


class FileExitManagement(models.Model):
    _name = "file.exit.management"
    _description = "File Exit Management"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    file_id = fields.Many2one('folder.master', string="File")
    file_name = fields.Char(string='File Name')
    number = fields.Char(string='Number')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('closed', 'Action Completed'),
         ('closed_part', 'Action Part Completed')
         ], string='Status')

    def file_forward(self):
        pass

