from odoo import models, fields, api


# File management
class CorrespondenceExitManagement(models.Model):
    _name = "correspondence.exit.management"
    _description = "Correspondence Exit Management"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    correspondence_id = fields.Many2one('muk_dms.file', string='Correspondence')
    letter_no = fields.Char(string="Letter Number")
    sender_type_id = fields.Many2one('doc.sender.type', string="Sender Type")
    file_assign_id = fields.Many2one('folder.master', string="File Assigned")

    def correspondence_forward(self):
        pass


class FileExitManagement(models.Model):
    _name = "file.exit.management"
    _description = "File Exit Management"

    exit_transfer_id = fields.Many2one("exit.transfer.management", string="Exit/Transfer Id", readonly=True)
    file_name = fields.Char(string='File Name')
    number = fields.Char(string='Number')
    status = fields.Selection([('normal', 'Normal'),
                               ('important', 'Important'),
                               ('urgent', 'Urgent')
                               ], string='Status', track_visibility='always')

    # def file_approved(self):
    #     if self.ltc_sequence_id:
    #         self.ltc_sequence_id.sudo().button_approved()
    #         self.update({"state": "approved"})


