from odoo import fields, models, api
from datetime import datetime

class CreateFolder(models.TransientModel):
    _name = 'assignfolder.wizard'
    _description = 'Wizard of Create folder'


    folder = fields.Many2one('folder.master', string = 'Folder')
    dg_id = fields.Many2one('green.sheets')
    deffolderid = fields.Many2one('muk_dms.file')
    datas = fields.Binary(related='deffolderid.pdf_file')




    def confirm_button(self):
        if self:
            pass
            # self.deffolderid.folder_id = self.folder.id
            #
            # return {
            #     'name': 'Note Sheet',
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'res_model': 'green.sheets',
            #     'type': 'ir.actions.act_window',
            #     'target': 'current',
            #     'context': ({
            #         'default_file_id': self.deffolderid.id,
            #         'default_file_no': self.deffolderid.name,
            #         'default_file_date': self.deffolderid.create_date,
            #         'default_folder_id': self.deffolderid.folder_id.id,
            #         'default_documenttype': self.deffolderid.documenttype,
            #         'default_datas': self.datas
            #     })
            # }
            #
