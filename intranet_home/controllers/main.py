from odoo import http
from odoo.addons.website.controllers.main import Website
from odoo.http import request
from odoo.addons.portal.controllers.web import Home

class Website(Home):

    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        # prefetch all menus (it will prefetch website.page too)
        website = request.env['website'].get_current_website()
        usefull_links = request.env['vardhman.useful.links'].sudo().search([], limit=6)
        birthday_links = request.env['vardhman.employee.birthday'].sudo().search([], limit=3)
        annivarsary_links = request.env['vardhman.employee.workanniversary'].sudo().search([], limit=3)
        BlogPost = request.env['blog.post']
        video_link = request.env['vardhman.videos.links'].search([], limit=3)
        magazine_link = request.env['vardhman.magazine.links'].search([], limit=3)
        photo_link = request.env['vardhman.photo.links'].search([], limit=3)
        slider_link = request.env['vardhman.slider.links'].search([], limit=3)
        event_link = request.env['event.event'].search([], limit=3)
        posts = BlogPost.search([], limit=3, order="is_published desc, post_date desc, id asc")
        if website.theme_id.name == 'intranet_home':
            return request.render('intranet_home.new_homepage_vardhman', {'usefull_links': usefull_links,
                'birthday_links': birthday_links,
                'annivarsary_links': annivarsary_links,
                'posts': posts,
                'event_link': event_link,
                'photo_link': photo_link,
                'slider_link': slider_link,
                'video_link': video_link,
                'magazine_link': magazine_link})
        homepage = request.website.homepage_id
        return request.render('website.homepage')