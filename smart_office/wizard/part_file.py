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
                    data = {
                        'assign_name': self.deffolderid.folder_name,
                        'assign_no': self.deffolderid.sequence,
                        'assign_date': self.deffolderid.date,
                        'assign_subject': (self.deffolderid.subject.subject),
                        'remarks': self.deffolderid.description,
                        'created_by': self.deffolderid.current_owner_id.id,
                        'doc_flow_id': 0,
                        'wing_id': self.deffolderid.department_id.id,
                        'section_id': 0,
                        'designation_id': self.deffolderid.job_id.id,
                        'document_ids': self.deffolderid.document_ids,
                    }
                    req = requests.post('http://103.92.47.152/STPI/www/web-service/add-assignment/', data=data,
                                        json=None)
                    try:
                        pastebin_url = req.text
                        print('============Patebin url=================', pastebin_url)
                        dictionary = json.loads(pastebin_url)
                    except Exception as e:
                        print('=============Error==========', e)
                for letter in file.document_dispatch:
                    letter.folder_id = self.deffolderid.id
                    self.deffolderid.document_dispatch = [(4, letter.id)]
                file.sudo().button_close_part()