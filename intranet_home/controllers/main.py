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
        work_links = request.env['vardhman.employee.workanniversary'].sudo().search([], limit=3)
        marriage_links = request.env['vardhman.employee.marriageanniversary'].sudo().search([], limit=3)
        BlogPost = request.env['blog.post']
        video_link = request.env['vardhman.videos.links'].search([], limit=3)
        magazine_link = request.env['vardhman.magazine.links'].search([], limit=3)
        photo_link = request.env['vardhman.photo.links'].search([], limit=3)
        slider_link = request.env['vardhman.slider.links'].search([], limit=3)
        event_link = request.env['event.event'].search([], limit=3)
        website_ids = request.env['website'].search([], limit=6)
        forum_links = request.env['forum.forum'].search([], limit=6)
        posts = BlogPost.search([('blog_id.front_type', '=', 'idea')], limit=3, order="is_published desc, post_date desc, id asc")
        calendar_first = BlogPost.search([('blog_id.front_type', '=', 'calendar_1')], limit=1, order="is_published desc, post_date desc, id asc")
        calendar_second = BlogPost.search([('blog_id.front_type', '=', 'calendar_2')], limit=1, order="is_published desc, post_date desc, id asc")
        calendar_third = BlogPost.search([('blog_id.front_type', '=', 'calendar_3')], limit=1, order="is_published desc, post_date desc, id asc")
        news_posts = BlogPost.search([('blog_id.front_type', '=', 'news')], limit=3, order="is_published desc, post_date desc, id asc")
        story_posts = BlogPost.search([('blog_id.front_type', '=', 'story')], limit=3, order="is_published desc, post_date desc, id asc")
        announcement_posts = BlogPost.search([('blog_id.front_type', '=', 'announcement')], limit=3, order="is_published desc, post_date desc, id asc")
        if website.theme_id.name == 'intranet_home':
            return request.render('intranet_home.new_homepage_vardhman', {'usefull_links': usefull_links,
                'birthday_links': birthday_links,
                'work_links': work_links,
                'marriage_links': marriage_links,
                'is_intranet': True,
                'posts': posts,
                'news_posts': news_posts,
                'website_ids': website_ids,
                'event_link': event_link,
                'photo_link': photo_link,
                'slider_link': slider_link,
                'video_link': video_link,
                'magazine_link': magazine_link,
                'story_posts': story_posts,
                'announcement_posts': announcement_posts,
                'calendar_first': calendar_first,
                'calendar_second': calendar_second,
                'calendar_third': calendar_third,
                'forum_links': forum_links})
        homepage = request.website.homepage_id
        return request.render('website.homepage')


    @http.route('/usefull/links', type='http', auth="public", website=True, sitemap=True)
    def usefull_links(self, **kw):
        # prefetch all menus (it will prefetch website.page too)
        usefull_links = request.env['vardhman.useful.links'].sudo().search([], )
        return request.render('intranet_home.usefull_links', {'usefull_links': usefull_links})

    @http.route('/birthday/links', type='http', auth="public", website=True, sitemap=True)
    def birthday_links(self, **kw):
        # prefetch all menus (it will prefetch website.page too)
        birthday_links = request.env['vardhman.employee.birthday'].sudo().search([], )
        return request.render('intranet_home.birthday_links', {'birthday_links': birthday_links})

    @http.route('/anniversary/links', type='http', auth="public", website=True, sitemap=True)
    def anniversary_links(self, **kw):
        # prefetch all menus (it will prefetch website.page too)
        anniversary_links = request.env['vardhman.employee.workanniversary'].sudo().search([], )
        marriage_links = request.env['vardhman.employee.marriageanniversary'].sudo().search([], )
        return request.render('intranet_home.anniversary_links', {'anniversary_links': anniversary_links, 'marriage_links': marriage_links})

    @http.route('/share/post', type='http', auth="public", website=True, sitemap=True)
    def share_post(self, **kw):
        # prefetch all menus (it will prefetch website.page too)
        usefull_links = request.env['vardhman.useful.links'].sudo().search([], )
        # anniversary_links = request.env['vardhman.employee.workanniversary'].sudo().search([], )
        return request.render('intranet_home.share_post_template', {'usefull_links': usefull_links})