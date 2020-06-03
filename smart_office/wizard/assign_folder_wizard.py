from odoo import fields, models, api
from datetime import datetime

class CreateFolder(models.TransientModel):
    _name = 'assign.folder.wizard'
    _description = 'Wizard of Create folder'


    deffolderid = fields.Many2one('muk_dms.file')
    cooespondence_ids = fields.Many2many('muk_dms.file', string='Correspondence')
    folder_id = fields.Many2one('folder.master', string="Select File")


    def confirm_button(self):
        if self:
            letter_id = []
            letter_id.append(self.deffolderid.id)
            self.folder_id.folder_ids = [(6, 0, letter_id)]
            form_view = self.env.ref('smart_office.foldermaster_form_view')
            tree_view = self.env.ref('smart_office.foldermaster_tree_view1')
            value = {
                'domain': str([('id', '=', self.folder_id.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'folder.master',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': self.folder_id.id,
                'target': 'current',
                'nodestroy': True
            }
            return value