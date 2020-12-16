from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug
from odoo.http import request
import jwt
import odoo
from odoo import models, fields, api, _

# key = 'chalhatpagle'
key = ",jy`\;4Xpe7%KKL$.VNJ'.s6)wErQa"

class IntermediateWebsitePage(http.Controller):
    @http.route(['/login/intermediate'], type='http', auth="user", website=True)
    def intermediate_detail(self, user_id=None, **post):
        user_id = request.env.user
        access_type=[]
        connection_rec=request.env['server.connection'].search([], limit=1)
        base_url= http.request.env["ir.config_parameter"].sudo().get_param("web.base.url").strip()
        url=str(connection_rec.url).strip()
        encoded_jwt = jwt.encode({'token': user_id.token}, key)
        coe,hrms,coe_hrms,coehrms,asset,services,floor,all = '','','','','','','',''
        for access in user_id.access_type_ids:
            if access.name == 'COE':
                coe = 'COE'
            if access.name == 'HRMS':
                hrms = 'HRMS'
            if access.name == 'COE And HRMS':
                coe_hrms = 'COE And HRMS'
            if access.name == 'STPI Next':
               coehrms = 'COE With HRMS'
            if access.name == 'Asset':
               asset = 'Asset'
            if access.name == 'Services':
               services = 'Services'
            if access.name == 'Floor Plan':
                floor = 'Floor Plan'
        asset_id = http.request.env['ir.model.data'].sudo().search([('name','=','action_account_asset_asset_form'),('module','=','account_asset')])
        service_id = http.request.env['ir.model.data'].sudo().search([('name','=','action_comman_available_service_menu'),('module','=','coe_service_management')])
        asset_url = http.request.env["ir.config_parameter"].sudo().get_param("web.base.url").strip()
        asset_url += ('/web#id='  + '&action=' +str(asset_id.res_id) + '&model=account.asset.assets&view_type=list')
        service_url =base_url + ('/web#id='  + '&action=' + str(service_id.res_id) + '&model=product.product&view_type=kanban')

        if user_id:
            partner_sudo = request.env['res.users'].sudo().browse(user_id)
            if partner_sudo.exists():
                values = {
                    'login_user': partner_sudo,
                    'access_type': access_type,
                    'edit_page': True,
                    'coe' :coe,
                    'hrms' :hrms,
                    'coe_hrms' :coe_hrms,
                    'coehrms' :coehrms,
                    'all' :all,
                    'services' :services,
                    'asset' :asset,
                    'floor' :floor,
                    'url': url,
                    'asset_url': asset_url,
                    'service_url': service_url,
                    'base_url': base_url,
                    'login':request.env.user.login,
                    'instance_type':connection_rec.instance_type,
                    'password':str(encoded_jwt.decode("utf-8"))
                }
                return request.render("gts_switcher.intermediate_page", values)
        return request.not_found()

