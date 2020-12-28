# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import http, _
from operator import itemgetter
from odoo.addons.http_routing.models.ir_http import slug
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class teldirData(CustomerPortal):

    def _prepare_portal_layout_values(self):
        teldirs_count = 0
        values = super(teldirData, self)._prepare_portal_layout_values()
        teldirs_count = request.env['hr.employee'].sudo().search_count([])
        values['teldirs_count'] = teldirs_count
        values['page_name'] = 'teldirs'
        return values

    @http.route(['/get/teldirs', '/get/teldirs/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_teldir(self, page=1, access_token=None, search=None, search_in='all', sortby=None, groupby='none', **kw):
        values = self._prepare_portal_layout_values()
        teldir_obj = request.env['hr.employee']
        teldirs_count = 0
        domain = [('id', '!=', 0)]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'job_id': {'label': _('Job Position'), 'order': 'job_id desc'},
            'unit_id': {'label': _('Unit'), 'order': 'unit_id desc'},
            'department_id': {'label': _('Department'), 'order': 'department_id desc'},
        }

        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
            'job_id': {'input': 'job_id', 'label': _('Search by Job Position')},
            'name': {'input': 'name', 'label': _('Search by Name')},
            'unit_id': {'input': 'unit_id', 'label': _('Search by Unit')},
            'department_id': {'input': 'department_id', 'label': _('Search by Department')},
            'work_mobile': {'input': 'work_mobile', 'label': _('Search by Work Mobile')},
            'work_phone': {'input': 'work_phone', 'label': _('Search by Work Phone')},
            'work_email': {'input': 'work_email', 'label': _('Search by Work Email')},
        }

        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        teldirs_count = teldir_obj.search_count(domain)

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('job_id', 'all'):
                search_domain = OR([search_domain, [('job_id', 'ilike', search)]])
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('unit_id', 'all'):
                search_domain = OR([search_domain, [('unit_id', 'ilike', search)]])
            if search_in in ('department_id', 'all'):
                search_domain = OR([search_domain, [('department_id', 'ilike', search)]])
            if search_in in ('work_mobile', 'all'):
                search_domain = OR([search_domain, [('work_mobile', 'ilike', search)]])
            if search_in in ('work_phone', 'all'):
                search_domain = OR([search_domain, [('work_phone', 'ilike', search)]])
            if search_in in ('work_email', 'all'):
                search_domain = OR([search_domain, [('work_email', 'ilike', search)]])
            domain += search_domain

        pager = portal_pager(
            url="/get/teldirs",
            total=teldirs_count,
            page=page,
            url_args={'search_in': search_in, 'search': search},
            step=12
        )

        # content according to pager and archive selected
        teldirs_ids = teldir_obj.search(domain, order=order, limit=12, offset=pager['offset'])
        values.update({
            'teldirs_ids': teldirs_ids,
            'page_name': 'teldirs',
            'teldirs_count': teldirs_count,
            'pager': pager,
            'default_url': '/get/teldirs',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
        })
        return request.render("portal_teldir_management.portal_my_teldirs_data", values)