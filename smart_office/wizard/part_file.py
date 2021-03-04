from odoo import fields, models, api
from datetime import datetime
import requests
import json

class CreateFolder(models.TransientModel):
    _name = 'part.file.wizard'
    _description = 'Wizard of Part File'


    deffolderid = fields.Many2one('folder.master')
    folder_id = fields.Many2many('folder.master', string="Select File")
    description = fields.Text(string = 'Description')


    def confirm_button(self):
        if self:
            for file in self.folder_id:
                for letter in file.file_ids:
                    letter.folder_id = self.deffolderid.id
                    self.deffolderid.file_ids = [(4, letter.id)]
                    self.deffolderid.document_ids = str(self.deffolderid.document_ids) + ',' + str(letter.php_letter_id)
                for letter in file.document_dispatch:
                    letter.folder_id = self.deffolderid.id
                    self.deffolderid.document_dispatch = [(4, letter.id)]
                file.sudo().button_close_part()