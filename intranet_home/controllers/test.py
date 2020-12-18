from odoo import http
from odoo.addons.website.controllers.main import Website

class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public')
    def index(self, **kw):
        return "Hello, world"

class AcademyTwo(http.Controller):
    @http.route('/academy/academytwo/', auth='public')
    def index(self, **kw):
        return http.request.render('intranet_home.indextwo', {
            'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
        })

class AcademyThree(http.Controller):
    @http.route('/academy/academythree/', auth='public')
    def index(self, **kw):
        Teachers = http.request.env['vardhman.useful.links']
        return http.request.render('intranet_home.indexthree', {
            'teachers': Teachers.search([])
        })

class AcademyFour(http.Controller):
    @http.route('/academy/academyfour/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['vardhman.useful.links']
        return http.request.render('intranet_home.indexfour', {
            'teachers': Teachers.search([])
        })

    @http.route('/academy/<name>/', auth='public', website=True)
    def teacher(self, name):
        return '<h1>{}</h1>'.format(name)
