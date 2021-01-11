# -*- coding: utf-8 -*-

import base64
from odoo.http import request
from odoo import http, _
from operator import itemgetter
from odoo.addons.http_routing.models.ir_http import slug
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class DocumentData(CustomerPortal):

    def _prepare_portal_layout_values(self):
        documents_count = 0
        values = super(DocumentData, self)._prepare_portal_layout_values()
        documents_count = request.env['portal.documents'].sudo().search_count([('parent_id', '=', False)])
        values['documents_count'] = documents_count
        values['page_name'] = 'documents'
        return values

    @http.route(['/get/documents', '/get/documents/<model("portal.documents"):folder>', '/get/documents/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_document(self, folder=None, page=1, access_token=None, search=None, search_in='all', sortby=None, groupby='none', **kw):
        values = self._prepare_portal_layout_values()
        document_obj = request.env['portal.documents']
        documents_count = 0
        domain = [('parent_id', '=', False)]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name asc'},
            # 'type': {'label': _('Type'), 'order': 'type_id desc'},
            'create_uid': {'label': _('Published By'), 'order': 'create_uid desc'},
            'create_date': {'label': _('Published'), 'order': 'create_date desc'},
        }

        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
            # 'type': {'input': 'type_id', 'label': _('Search by Type')},
            'name': {'input': 'name', 'label': _('Search by Name')},
        }

        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        documents_count = document_obj.search_count(domain)

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            # if search_in in ('type_id', 'all'):
            #     search_domain = OR([search_domain, [('type_id', 'ilike', search)]])
            domain += search_domain

        pager = portal_pager(
            url="/get/documents",
            total=documents_count,
            page=page,
            url_args={'search_in': search_in, 'search': search},
            step=12
        )

        # content according to pager and archive selected
        documents_ids = document_obj.search(domain, order=order, limit=12, offset=pager['offset'])
        folder_ids = request.env['portal.documents'].search([])
        parent_folder_ids = request.env['portal.documents'].search([('parent_id', '=', False)])
        if folder:
            parent_folder_ids = request.env['portal.documents'].search([('parent_id', '=', folder.id)])
        usefull_links = request.env['vardhman.useful.links'].sudo().search([], limit=6)
        values.update({
            'parent_folder_ids': parent_folder_ids,
            'documents_ids': documents_ids,
            'page_name': 'documents',
            'documents_count': documents_count,
            'pager': pager,
            'default_url': '/get/documents',
            # 'searchbar_sortings': searchbar_sortings,
            # 'sortby': sortby,
            # 'search_in': search_in,
            # 'searchbar_inputs': searchbar_inputs,
            'folder_ids': folder_ids,
            'usefull_links': usefull_links,
        })
        return request.render("document_management.portal_my_documents_data", values)


    @http.route(['/create/folder'], type='http', auth="user", website=True, csrf=False)
    def portal_create_folder(self, access_token=None, **kw):

        if kw:
            folder_id = request.env['portal.documents'].create({'name': kw.get('name'), 'parent_id': kw.get('parent_id', False)})
        return request.redirect('/get/documents')


    @http.route(['/upload/document'], type='http', auth="user", website=True, csrf=False)
    def portal_upload_document(self, access_token=None, **kw):
        folder_id = request.env['portal.documents'].browse(int(kw.get('parent_id')))
        if kw:
            ufile = kw.get('ufile').read()
            attachment_id = request.env['documents.attachment'].create({'name': kw.get('ufile').filename, 'document': base64.b64encode(ufile), 'parent_id': folder_id.id})
        return request.redirect('/get/documents/%s' % slug(folder_id))