from odoo import http
from odoo.http import request
import json


@http.route(['/files/forward'], type='json', auth='public', methods=['POST'])
def get_forward_details(self, **kwargs):
    forward_details_data = request.env['folder.tracking.information'].search([])
    foward_det = []
    for rec in forward_details_data:
        vals={
            'id': rec.id,
            'forwarded_by': rec.forwarded_by,
            'forwarded_date': rec.forwarded_date,
            'forwarded_to_user': rec.forwarded_to_user,
            'forwarded_to_dept': rec.forwarded_to_dept,
            'create_let_id': rec.create_let_id,
        }
        foward_det.append(vals)
        data = {'status': 200, 'response': foward_det, 'message': 'Success'}
        return data
