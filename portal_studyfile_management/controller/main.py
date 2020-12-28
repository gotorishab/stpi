# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import http, _
from operator import itemgetter
from odoo.addons.http_routing.models.ir_http import slug
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class studyfileData(CustomerPortal):

    def _prepare_portal_layout_values(self):
        studyfiles_count = 0
        values = super(studyfileData, self)._prepare_portal_layout_values()
        studyfiles_count = request.env['portal.studyfiles'].sudo().search_count([('is_published', '=', True)])
        values['studyfiles_count'] = studyfiles_count
        values['page_name'] = 'studyfiles'
        return values

    @http.route(['/get/studyfiles', '/get/studyfiles/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_studyfile(self, page=1, access_token=None, search=None, search_in='all', sortby=None, groupby='none', **kw):
        values = self._prepare_portal_layout_values()
        studyfile_obj = request.env['portal.studyfiles']
        studyfiles_count = 0
        domain = [('is_published', '=', True)]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'type': {'label': _('Type'), 'order': 'type_id desc'},
            'create_uid': {'label': _('Published By'), 'order': 'create_uid desc'},
            'create_date': {'label': _('Published'), 'order': 'create_date desc'},
        }

        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
            'type': {'input': 'type_id', 'label': _('Search by Type')},
            'name': {'input': 'name', 'label': _('Search by Name')},
        }

        if not sortby:
            sortby = 'type'
        order = searchbar_sortings[sortby]['order']

        studyfiles_count = studyfile_obj.search_count(domain)

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('type_id', 'all'):
                search_domain = OR([search_domain, [('type_id', 'ilike', search)]])
            domain += search_domain

        pager = portal_pager(
            url="/get/studyfiles",
            total=studyfiles_count,
            page=page,
            url_args={'search_in': search_in, 'search': search},
            step=12
        )

        # content according to pager and archive selected
        studyfiles_ids = studyfile_obj.search(domain, order=order, limit=12, offset=pager['offset'])
        values.update({
            'studyfiles_ids': studyfiles_ids,
            'page_name': 'studyfiles',
            'studyfiles_count': studyfiles_count,
            'pager': pager,
            'default_url': '/get/studyfiles',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
        })
        return request.render("portal_studyfile_management.portal_my_studyfiles_data", values)