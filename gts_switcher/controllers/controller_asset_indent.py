import odoo
from odoo import http, modules, tools
from odoo.http import request
from odoo.osv import expression
from odoo import models, fields, api, _

class AssetIndent(http.Controller):
    @http.route('/asset/indent', type='http', auth="none", sitemap=False)
    def asset_detail(self, redirect=None, **kw):
        old_uid = False
        try:
            uid = request.session.authenticate(request.session.db, kw.get('login'), kw.get('password'))
            request.params['login_success'] = True
            return http.redirect_with_hash(self._asset_redirect(uid, redirect=redirect, asset_id=kw.get('menu_id')))
        except odoo.exceptions.AccessDenied as e:
            request.uid = old_uid
            values = {'login_user': request.uid, }
            return request.render("gts_switcher.intermediate_login_fail_page", values)

    def _asset_redirect(self, uid, redirect=None,asset_id=None):
        url = http.request.env["ir.config_parameter"].sudo().get_param("web.base.url").strip()
        assei_form_id = http.request.env['ir.model.data'].sudo().search([('module', '=', 'account_asset'),('model','=','ir.actions.act_window')],limit=1)
        asset_url = url + ('/web#id=' + str(asset_id) + '&action=' + str( assei_form_id.res_id) + '&model=account.asset.asset&view_type=form')
        return asset_url

