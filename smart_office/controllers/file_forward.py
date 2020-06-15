from odoo import http
from odoo.http import request
import json

class FileForwardData(http.Controller):
    @http.route(['/filesforward'], type='json', auth='public', csrf=False, methods=['POST'])
    def get_forward_details(self, **kwargs):
        forward_details_data = request.env['folder.tracking.information'].sudo().search([])
        foward_det = []
        for rec in forward_details_data:
            vals={
                'id': rec.id,
                'forwarded_by': rec.forwarded_by,
                'forwarded_date': rec.forwarded_date,
                'forwarded_to_user': rec.forwarded_to_user,
                'forwarded_to_dept': rec.forwarded_to_dept,
                'file_id': rec.create_let_id,
            }
            foward_det.append(vals)
        data = {'status': 200, 'response': foward_det, 'message': 'Success'}
        return data

    @http.route(['/letterlist'], type='json', auth='public', csrf=False, methods=['POST'])
    def get_letter_list_details(self, **kwargs):
        letter_details_data = request.env['muk_dms.file'].sudo().search([])
        letter_det = []
        for rec in letter_details_data:
            vals={
                'id': rec.id,
                'attachment': rec.content,
            }
            letter_det.append(vals)
        data = {'status': 200, 'response': letter_det, 'message': 'Success'}
        return data

    @http.route(['/closedfile'], type='json', auth='public', csrf=False, methods=['POST'])
    def get_closed_file(self, **kwargs):
        forward_details_data = request.env['folder.master'].sudo().search([('state', '=', 'closed')])
        foward_det = []
        for rec in forward_details_data:
            vals={
                'id': rec.id,
                'folder_name': rec.folder_name,
                'number': rec.number,
                'current_owner_id': rec.current_owner_id.id,
            }
            foward_det.append(vals)
        data = {'status': 200, 'response': foward_det, 'message': 'Success'}
        return data