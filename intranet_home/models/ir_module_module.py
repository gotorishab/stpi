# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def _theme_remove(self, website):
        """
            Remove from ``website`` its current theme, including all the themes in the stream.
        """
        home_template = self.env.ref('intranet_home.new_homepage_vardhman')
        assets_template = self.env.ref('intranet_home.assets_frontend')

        if website.theme_id.name == 'intranet_home'and home_template:
            home_template.active = False
            assets_template.active = False
        return super(IrModuleModule, self)._theme_remove(website)

    def button_choose_theme(self):
        """
            Active oxidine header  theme on the current website.
        """
        website = self.env['website'].get_current_website()
        home_template = self.env.ref('intranet_home.new_homepage_vardhman')
        assets_template = self.env.ref('intranet_home.assets_frontend')
        if self.name == 'intranet_home' and home_template:
            home_template.active = True
            assets_template.active = True
        return super(IrModuleModule, self).button_choose_theme()
