from odoo import http
from odoo.addons.website.controllers.main import Website
from odoo.http import request
from odoo.addons.portal.controllers.web import Home

class Website(Website):

    @http.route(auth='public')
    def index(self, data={}, **kw):
        super(Website, self).index(**kw)
        return http.request.render('intranet_home.new_homepage_vardhman', data)



class Academy(http.Controller):
    @http.route('/usefullinks/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['vardhman.useful.links']
        Employees = http.request.env['hr.employee']
        return http.request.render('intranet_home.use_links', {
            'teachers': Teachers.search([])
        })


class home(Home):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        print("<<<<<<<<<<<<<<<<<<<")
        links = request.env['vardhman.useful.links'].sudo().search([])
        birthlink = request.env['vardhman.employee.birthday'].sudo().search([])
        print("----------",links)
        if links:
            values = [{
                'name':x['name'],
                'url':x['url'],
                'icon':x['icon'],
                #'icon':links.icon
            } for x in links]
        if birthlink:
            birthvalues = [{
                'name':x['name'],
                'image':x['image'],
                'job_title':x['job_title'],
                'birthday':x['birthday'],
            } for x in birthlink]
        return request.render('intranet_home.new_homepage_vardhman', {'values':values,'birthvalues':birthvalues})